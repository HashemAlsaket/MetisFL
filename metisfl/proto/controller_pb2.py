# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metisfl/proto/controller.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from metisfl.proto import model_pb2 as metisfl_dot_proto_dot_model__pb2
from metisfl.proto import learner_pb2 as metisfl_dot_proto_dot_learner__pb2
from metisfl.proto import service_common_pb2 as metisfl_dot_proto_dot_service__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1emetisfl/proto/controller.proto\x12\x07metisfl\x1a\x19metisfl/proto/model.proto\x1a\x1bmetisfl/proto/learner.proto\x1a\"metisfl/proto/service_common.proto\"\xdd\x01\n\x07Learner\x12\x1a\n\x08hostname\x18\x01 \x01(\tR\x08hostname\x12\x12\n\x04port\x18\x02 \x01(\rR\x04port\x12\x34\n\x16root_certificate_bytes\x18\x03 \x01(\tR\x14rootCertificateBytes\x12\x38\n\x18public_certificate_bytes\x18\x04 \x01(\tR\x16publicCertificateBytes\x12\x32\n\x15num_training_examples\x18\x05 \x01(\rR\x13numTrainingExamples\"\x1b\n\tLearnerId\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\"\xa7\x01\n\x10TrainDoneRequest\x12\x1d\n\nlearner_id\x18\x01 \x01(\tR\tlearnerId\x12\x17\n\x07task_id\x18\x02 \x01(\tR\x06taskId\x12$\n\x05model\x18\x03 \x01(\x0b\x32\x0e.metisfl.ModelR\x05model\x12\x35\n\x08metadata\x18\x04 \x01(\x0b\x32\x19.metisfl.TrainingMetadataR\x08metadata\"\xf5\x02\n\x10TrainingMetadata\x12@\n\x07metrics\x18\x01 \x03(\x0b\x32&.metisfl.TrainingMetadata.MetricsEntryR\x07metrics\x12)\n\x10\x63ompleted_epochs\x18\x02 \x01(\x02R\x0f\x63ompletedEpochs\x12+\n\x11\x63ompleted_batches\x18\x03 \x01(\rR\x10\x63ompletedBatches\x12\x1d\n\nbatch_size\x18\x04 \x01(\rR\tbatchSize\x12\x35\n\x17processing_ms_per_epoch\x18\x05 \x01(\x02R\x14processingMsPerEpoch\x12\x35\n\x17processing_ms_per_batch\x18\x06 \x01(\x02R\x14processingMsPerBatch\x1a:\n\x0cMetricsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\"\xa7\x05\n\x04Logs\x12K\n\x10task_learner_map\x18\x01 \x03(\x0b\x32!.metisfl.Logs.TaskLearnerMapEntryR\x0etaskLearnerMap\x12P\n\x11training_metadata\x18\x02 \x03(\x0b\x32#.metisfl.Logs.TrainingMetadataEntryR\x10trainingMetadata\x12V\n\x13\x65valuation_metadata\x18\x03 \x03(\x0b\x32%.metisfl.Logs.EvaluationMetadataEntryR\x12\x65valuationMetadata\x12G\n\x0emodel_metadata\x18\x04 \x03(\x0b\x32 .metisfl.Logs.ModelMetadataEntryR\rmodelMetadata\x1a\x41\n\x13TaskLearnerMapEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\tR\x05value:\x02\x38\x01\x1a^\n\x15TrainingMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12/\n\x05value\x18\x02 \x01(\x0b\x32\x19.metisfl.TrainingMetadataR\x05value:\x02\x38\x01\x1a\x62\n\x17\x45valuationMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.metisfl.EvaluationMetadataR\x05value:\x02\x38\x01\x1aX\n\x12ModelMetadataEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x16.metisfl.ModelMetadataR\x05value:\x02\x38\x01\"\xfd\x02\n\rModelMetadata\x12\x32\n\x15selection_duration_ms\x18\x02 \x01(\x01R\x13selectionDurationMs\x12\x36\n\x17\x61ggregation_duration_ms\x18\x03 \x01(\x01R\x15\x61ggregationDurationMs\x12\x34\n\x16\x61ggregation_block_size\x18\x0f \x03(\x01R\x14\x61ggregationBlockSize\x12=\n\x1b\x61ggregation_block_memory_kb\x18\x10 \x03(\x01R\x18\x61ggregationBlockMemoryKb\x12\x41\n\x1d\x61ggregation_block_duration_ms\x18\x11 \x03(\x01R\x1a\x61ggregationBlockDurationMs\x12H\n\x12tensor_quantifiers\x18\x12 \x03(\x0b\x32\x19.metisfl.TensorQuantifierR\x11tensorQuantifiers2\xab\x03\n\x11\x43ontrollerService\x12\x31\n\x0fGetHealthStatus\x12\x0e.metisfl.Empty\x1a\x0c.metisfl.Ack\"\x00\x12\x31\n\x0fSetInitialModel\x12\x0e.metisfl.Model\x1a\x0c.metisfl.Ack\"\x00\x12\x38\n\x0eJoinFederation\x12\x10.metisfl.Learner\x1a\x12.metisfl.LearnerId\"\x00\x12\x35\n\x0fLeaveFederation\x12\x12.metisfl.LearnerId\x1a\x0c.metisfl.Ack\"\x00\x12/\n\rStartTraining\x12\x0e.metisfl.Empty\x1a\x0c.metisfl.Ack\"\x00\x12\x36\n\tTrainDone\x12\x19.metisfl.TrainDoneRequest\x1a\x0c.metisfl.Ack\"\x00\x12*\n\x07GetLogs\x12\x0e.metisfl.Empty\x1a\r.metisfl.Logs\"\x00\x12*\n\x08ShutDown\x12\x0e.metisfl.Empty\x1a\x0c.metisfl.Ack\"\x00\x62\x06proto3')



_LEARNER = DESCRIPTOR.message_types_by_name['Learner']
_LEARNERID = DESCRIPTOR.message_types_by_name['LearnerId']
_TRAINDONEREQUEST = DESCRIPTOR.message_types_by_name['TrainDoneRequest']
_TRAININGMETADATA = DESCRIPTOR.message_types_by_name['TrainingMetadata']
_TRAININGMETADATA_METRICSENTRY = _TRAININGMETADATA.nested_types_by_name['MetricsEntry']
_LOGS = DESCRIPTOR.message_types_by_name['Logs']
_LOGS_TASKLEARNERMAPENTRY = _LOGS.nested_types_by_name['TaskLearnerMapEntry']
_LOGS_TRAININGMETADATAENTRY = _LOGS.nested_types_by_name['TrainingMetadataEntry']
_LOGS_EVALUATIONMETADATAENTRY = _LOGS.nested_types_by_name['EvaluationMetadataEntry']
_LOGS_MODELMETADATAENTRY = _LOGS.nested_types_by_name['ModelMetadataEntry']
_MODELMETADATA = DESCRIPTOR.message_types_by_name['ModelMetadata']
Learner = _reflection.GeneratedProtocolMessageType('Learner', (_message.Message,), {
  'DESCRIPTOR' : _LEARNER,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.Learner)
  })
_sym_db.RegisterMessage(Learner)

LearnerId = _reflection.GeneratedProtocolMessageType('LearnerId', (_message.Message,), {
  'DESCRIPTOR' : _LEARNERID,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.LearnerId)
  })
_sym_db.RegisterMessage(LearnerId)

TrainDoneRequest = _reflection.GeneratedProtocolMessageType('TrainDoneRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRAINDONEREQUEST,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.TrainDoneRequest)
  })
_sym_db.RegisterMessage(TrainDoneRequest)

TrainingMetadata = _reflection.GeneratedProtocolMessageType('TrainingMetadata', (_message.Message,), {

  'MetricsEntry' : _reflection.GeneratedProtocolMessageType('MetricsEntry', (_message.Message,), {
    'DESCRIPTOR' : _TRAININGMETADATA_METRICSENTRY,
    '__module__' : 'metisfl.proto.controller_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.TrainingMetadata.MetricsEntry)
    })
  ,
  'DESCRIPTOR' : _TRAININGMETADATA,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.TrainingMetadata)
  })
_sym_db.RegisterMessage(TrainingMetadata)
_sym_db.RegisterMessage(TrainingMetadata.MetricsEntry)

Logs = _reflection.GeneratedProtocolMessageType('Logs', (_message.Message,), {

  'TaskLearnerMapEntry' : _reflection.GeneratedProtocolMessageType('TaskLearnerMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _LOGS_TASKLEARNERMAPENTRY,
    '__module__' : 'metisfl.proto.controller_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.Logs.TaskLearnerMapEntry)
    })
  ,

  'TrainingMetadataEntry' : _reflection.GeneratedProtocolMessageType('TrainingMetadataEntry', (_message.Message,), {
    'DESCRIPTOR' : _LOGS_TRAININGMETADATAENTRY,
    '__module__' : 'metisfl.proto.controller_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.Logs.TrainingMetadataEntry)
    })
  ,

  'EvaluationMetadataEntry' : _reflection.GeneratedProtocolMessageType('EvaluationMetadataEntry', (_message.Message,), {
    'DESCRIPTOR' : _LOGS_EVALUATIONMETADATAENTRY,
    '__module__' : 'metisfl.proto.controller_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.Logs.EvaluationMetadataEntry)
    })
  ,

  'ModelMetadataEntry' : _reflection.GeneratedProtocolMessageType('ModelMetadataEntry', (_message.Message,), {
    'DESCRIPTOR' : _LOGS_MODELMETADATAENTRY,
    '__module__' : 'metisfl.proto.controller_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.Logs.ModelMetadataEntry)
    })
  ,
  'DESCRIPTOR' : _LOGS,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.Logs)
  })
_sym_db.RegisterMessage(Logs)
_sym_db.RegisterMessage(Logs.TaskLearnerMapEntry)
_sym_db.RegisterMessage(Logs.TrainingMetadataEntry)
_sym_db.RegisterMessage(Logs.EvaluationMetadataEntry)
_sym_db.RegisterMessage(Logs.ModelMetadataEntry)

ModelMetadata = _reflection.GeneratedProtocolMessageType('ModelMetadata', (_message.Message,), {
  'DESCRIPTOR' : _MODELMETADATA,
  '__module__' : 'metisfl.proto.controller_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.ModelMetadata)
  })
_sym_db.RegisterMessage(ModelMetadata)

_CONTROLLERSERVICE = DESCRIPTOR.services_by_name['ControllerService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRAININGMETADATA_METRICSENTRY._options = None
  _TRAININGMETADATA_METRICSENTRY._serialized_options = b'8\001'
  _LOGS_TASKLEARNERMAPENTRY._options = None
  _LOGS_TASKLEARNERMAPENTRY._serialized_options = b'8\001'
  _LOGS_TRAININGMETADATAENTRY._options = None
  _LOGS_TRAININGMETADATAENTRY._serialized_options = b'8\001'
  _LOGS_EVALUATIONMETADATAENTRY._options = None
  _LOGS_EVALUATIONMETADATAENTRY._serialized_options = b'8\001'
  _LOGS_MODELMETADATAENTRY._options = None
  _LOGS_MODELMETADATAENTRY._serialized_options = b'8\001'
  _LEARNER._serialized_start=136
  _LEARNER._serialized_end=357
  _LEARNERID._serialized_start=359
  _LEARNERID._serialized_end=386
  _TRAINDONEREQUEST._serialized_start=389
  _TRAINDONEREQUEST._serialized_end=556
  _TRAININGMETADATA._serialized_start=559
  _TRAININGMETADATA._serialized_end=932
  _TRAININGMETADATA_METRICSENTRY._serialized_start=874
  _TRAININGMETADATA_METRICSENTRY._serialized_end=932
  _LOGS._serialized_start=935
  _LOGS._serialized_end=1614
  _LOGS_TASKLEARNERMAPENTRY._serialized_start=1263
  _LOGS_TASKLEARNERMAPENTRY._serialized_end=1328
  _LOGS_TRAININGMETADATAENTRY._serialized_start=1330
  _LOGS_TRAININGMETADATAENTRY._serialized_end=1424
  _LOGS_EVALUATIONMETADATAENTRY._serialized_start=1426
  _LOGS_EVALUATIONMETADATAENTRY._serialized_end=1524
  _LOGS_MODELMETADATAENTRY._serialized_start=1526
  _LOGS_MODELMETADATAENTRY._serialized_end=1614
  _MODELMETADATA._serialized_start=1617
  _MODELMETADATA._serialized_end=1998
  _CONTROLLERSERVICE._serialized_start=2001
  _CONTROLLERSERVICE._serialized_end=2428
# @@protoc_insertion_point(module_scope)
