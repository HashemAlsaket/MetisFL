#include "metisfl/controller/core/learner_manager.h"

namespace metisfl::controller {

// Constructor
LearnerManager::LearnerManager()
    : learners_(),
      learners_stub_(),
      train_params_(),
      eval_params_(),
      learners_mutex_(),
      scheduling_pool_(2),
      train_tasks_cq_(),
      eval_tasks_cq_() {
  std::thread run_tasks_digest_t_(&LearnerManager::DigestTrainResponses, this);
  std::thread eval_tasks_digest_t_(&LearnerManager::DigestEvaluateResponses,
                                   this);
  run_tasks_digest_t_.detach();
  eval_tasks_digest_t_.detach();
}

// Public methods
absl::StatusOr<std::string> LearnerManager::AddLearner(const Learner &learner) {
  std::lock_guard<std::mutex> learners_guard(learners_mutex_);

  std::string learner_id =
      GenerateLearnerId(learner.hostname(), learner.port());

  if (learners_.contains(learner_id)) {
    return absl::AlreadyExistsError("Learner has already joined.");
  }

  learners_[learner_id] = learner;
  learners_stub_[learner_id] = CreateLearnerStub(learner_id);

  return learner_id;
}

std::vector<std::string> LearnerManager::GetLearnerIds() const {
  std::vector<std::string> learner_ids;
  for (const auto &[key, learner] : learners_) {
    learner_ids.push_back(key);
  }
  return learner_ids;
}

absl::Status LearnerManager::RemoveLearner(const std::string &learner_id) {
  std::lock_guard<std::mutex> learners_guard(learners_mutex_);

  if (!learners_.contains(learner_id)) {
    return absl::NotFoundError("Learner does not exist.");
  }

  learners_.erase(learner_id);
  learners_stub_.erase(learner_id);
  train_params_.erase(learner_id);
  eval_params_.erase(learner_id);

  return absl::OkStatus();
}

void LearnerManager::ScheduleAll(const Model &model) {
  Schedule(GetLearnerIds(), model);
}

void LearnerManager::Schedule(const std::vector<std::string> &learner_ids,
                              const Model &model) {
  scheduling_pool_.push_task(
      [this, learner_ids, model] { ScheduleTasks(learner_ids, model); });
}

void LearnerManager::Shutdown() {
  train_tasks_cq_.Shutdown();
  eval_tasks_cq_.Shutdown();
  scheduling_pool_.wait_for_tasks();
}

void LearnerManager::UpdateMetadata(const std::string &task_id,
                                    const std::string &learner_id,
                                    const TrainingMetadata &metadata) {
  num_completed_batches_[learner_id] = metadata.completed_batches();
  training_metadata_[task_id] = metadata;
}

absl::flat_hash_map<std::string, int> LearnerManager::GetNumTrainingExamples(
    const std::vector<std::string> &learner_ids) {
  absl::flat_hash_map<std::string, int> num_training_examples;

  for (const auto &learner_id : learner_ids) {
    num_training_examples[learner_id] =
        learners_[learner_id].num_training_examples();
  }

  return num_training_examples;
}

absl::flat_hash_map<std::string, int> LearnerManager::GetNumCompletedBatches(
    const std::vector<std::string> &learner_ids) {
  absl::flat_hash_map<std::string, int> num_completed_batches;

  for (const auto &learner_id : learner_ids) {
    num_completed_batches[learner_id] = num_completed_batches_[learner_id];
  }

  return num_completed_batches;
}

// FIXME:
// void LearnerManager::UpdateLearnersTaskTemplates(
//     std::vector<std::string> &learners) {
//   const auto &communication_protocol =
//       global_train_params_.communication_protocol;
//   if (communication_protocol == "SemiSynchronous" &&
//       (global_iteration_ == 2 ||
//        global_train_params_.semi_sync_recompute_num_updates)) {
//     // Finds the slowest learner.
//     float ms_per_epoch_slowest = std::numeric_limits<float>::min();
//     for (const auto &learner_id : learners) {
//       const auto &metadata = training_metadata_[learner_id].front();
//       if (metadata.processing_ms_per_epoch() > ms_per_epoch_slowest) {
//         ms_per_epoch_slowest = metadata.processing_ms_per_epoch();
//       }
//     }

//     // Calculates the allowed time for training.
//     float t_max = static_cast<float>(global_train_params_.semi_sync_lambda) *
//                   ms_per_epoch_slowest;

//     // Updates the task templates based on the slowest learner.
//     for (const auto &learner_id : learners) {
//       const auto &metadata = training_metadata_[learner_id].front();

//       auto processing_ms_per_batch = metadata.processing_ms_per_batch();
//       if (processing_ms_per_batch == 0) {
//         PLOG(ERROR) << "Processing ms per batch is zero. Setting to 1.";
//         processing_ms_per_batch = 1;
//       }
//       int num_local_updates = std::ceil(t_max / processing_ms_per_batch);

//       auto &task_template = train_params_[learner_id];
//       task_template.set_num_local_updates(num_local_updates);
//     }
//   }
// }

// Private methods
LearnerStub LearnerManager::CreateLearnerStub(const std::string &learner_id) {
  auto hostname = learners_[learner_id].hostname();
  auto port = learners_[learner_id].port();
  auto target = absl::StrCat(hostname, ":", port);
  auto &root_certificate = learners_[learner_id].root_certificate_bytes();
  auto &public_certificate = learners_[learner_id].public_certificate_bytes();

  auto ssl_creds = grpc::InsecureChannelCredentials();

  if (!root_certificate.empty() && !public_certificate.empty()) {
    grpc::SslCredentialsOptions ssl_opts;
    ssl_opts.pem_root_certs = root_certificate;
    ssl_opts.pem_cert_chain = public_certificate;
    ssl_creds = grpc::SslCredentials(ssl_opts);
  }

  auto channel = grpc::CreateChannel(target, ssl_creds);
  return LearnerService::NewStub(channel);
}

bool LearnerManager::ValidateLearner(const std::string &learner_id) const {
  return learners_.contains(learner_id);
}

void LearnerManager::ScheduleTasks(const std::vector<std::string> &learner_ids,
                                   const Model &model) {
  for (const auto &learner_id : learner_ids) {
    std::lock_guard<std::mutex> learners_guard(learners_mutex_);

    SendTrainAsync(learner_id, model);

    // TODO: should we wait before sending the evaluation task?

    SendEvaluateAsync(learner_id, model);

    // UpdateLearnersTaskTemplates(to_schedule);
  }
}

void LearnerManager::SendTrainAsync(const std::string &learner_id,
                                    const Model &model) {
  TrainRequest request;
  *request.mutable_task_id() = metisfl::controller::GenerateRadnomId();
  *request.mutable_model() = model;
  *request.mutable_params() = train_params_[learner_id];

  auto *call = new AsyncLearnerRunTaskCall;
  auto &cq = train_tasks_cq_;
  auto learner_stub = CreateLearnerStub(learner_id);

  call->learner_id = learner_id;
  call->response_reader =
      learner_stub->PrepareAsyncTrain(&call->context, request, &cq);
  call->response_reader->StartCall();
  call->response_reader->Finish(&call->reply, &call->status, (void *)call);
}

void LearnerManager::DigestTrainResponses() {
  void *got_tag;
  bool ok = false;

  auto &cq_ = train_tasks_cq_;

  while (cq_.Next(&got_tag, &ok)) {
    auto *call = static_cast<AsyncLearnerRunTaskCall *>(got_tag);
    GPR_ASSERT(ok);

    if (call) {
      if (!call->status.ok()) {
        PLOG(ERROR) << "Train RPC request to learner: " << call->learner_id
                    << " failed with error: " << call->status.error_message();
      }
    }
    delete call;
  }
}

void LearnerManager::SendEvaluateAsync(const std::string &learner_id,
                                       const Model &model) {
  EvaluateRequest request;
  *request.mutable_task_id() = metisfl::controller::GenerateRadnomId();
  *request.mutable_model() = model;
  *request.mutable_params() = eval_params_[learner_id];

  auto *call = new AsyncLearnerEvalCall;
  auto &cq = eval_tasks_cq_;
  auto learner_stub = CreateLearnerStub(learner_id);

  call->learner_id = learner_id;
  call->response_reader =
      learner_stub->PrepareAsyncEvaluate(&call->context, request, &cq);
  call->response_reader->StartCall();
  call->response_reader->Finish(&call->reply, &call->status, (void *)call);
}

void LearnerManager::DigestEvaluateResponses() {
  void *got_tag;
  bool ok = false;

  auto &cq_ = eval_tasks_cq_;
  while (cq_.Next(&got_tag, &ok)) {
    auto *call = static_cast<AsyncLearnerEvalCall *>(got_tag);
    GPR_ASSERT(ok);

    if (call) {
      if (call->status.ok()) {
        const std::string &task_id = call->reply.task_id();
        evaluation_metadata_[task_id] = call->reply.metadata();
      } else {
        PLOG(ERROR) << "EvaluateModel RPC request to learner: "
                    << call->learner_id
                    << " failed with error: " << call->status.error_message();
      }
    }
    delete call;
  }
}

}  // namespace metisfl::controller