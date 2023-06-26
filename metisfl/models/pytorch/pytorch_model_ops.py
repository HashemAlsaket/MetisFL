import gc
from metisfl.models.model_proto_factory import ModelProtoFactory
from metisfl.utils.formatting import DictionaryFormatter
from metisfl.utils.proto_messages_factory import MetisProtoMessages

import torch

from metisfl.models.pytorch.helper import construct_dataset_pipeline
from metisfl.models.model_dataset import ModelDataset
from metisfl.models.model_ops import CompletedTaskStats, ModelOps
from metisfl.models.pytorch.wrapper import MetisTorchModel
from metisfl.proto import metis_pb2
from metisfl.utils.metis_logger import MetisLogger
from metisfl.models.utils import get_num_of_epochs

class PyTorchModelOps(ModelOps):
    
    def __init__(self, model_dir: str):
        self._model = MetisTorchModel.load(model_dir)

    def train_model(self,
                    train_dataset: ModelDataset,
                    learning_task_pb: metis_pb2.LearningTask,
                    hyperparameters_pb: metis_pb2.Hyperparameters):
        if not train_dataset:
            raise RuntimeError("Provided `dataset` for training is None.")
        MetisLogger.info("Starting model training.")

        total_steps = learning_task_pb.num_local_updates
        batch_size = hyperparameters_pb.batch_size
        dataset_size = train_dataset.get_size()
        epochs_num = get_num_of_epochs(total_steps, dataset_size, batch_size)
        dataset = construct_dataset_pipeline(train_dataset)
        
        self._model.train()
        train_res = self._model.fit(dataset, epochs=epochs_num)
        
        # TODO (dstripelis) Need to add the metrics for computing the execution time
        #   per batch and epoch.
        model_weights_descriptor = self.get_model_weights()
        completed_learning_task = ModelProtoFactory.CompletedLearningTaskProtoMessage(
            weights_values=model_weights_descriptor.weights_values,
            weights_trainable=model_weights_descriptor.weights_trainable,
            weights_names=model_weights_descriptor.weights_names,
            train_stats=train_res,
            completed_epochs=epochs_num,
            global_iteration=learning_task_pb.global_iteration)
        completed_learning_task_pb = completed_learning_task.construct_completed_learning_task_pb(
            he_scheme=self._he_scheme)
        MetisLogger.info("Model training is complete.")
        return completed_learning_task_pb

    def evaluate_model(self, eval_dataset: ModelDataset):
        if not eval_dataset:
            raise RuntimeError("Provided `dataset` for evaluation is None.")
        MetisLogger.info("Starting model evaluation.")
        dataset = construct_dataset_pipeline(eval_dataset)
        self._model.eval()
        eval_res = self._model.evaluate(dataset)            
        MetisLogger.info("Model evaluation is complete.")
        metric_values = DictionaryFormatter.stringify(eval_res, stringify_nan=True)
        return MetisProtoMessages.construct_model_evaluation_pb(metric_values)
    
    def infer_model(self):
        # Set model to evaluation state.
        # FIXME @panoskyriakis: check this
        self._model.eval()
        pass

    # @stripeli do we really need this?
    def cleanup(self):
        del self._model
        torch.cuda.empty_cache()
        gc.collect()
