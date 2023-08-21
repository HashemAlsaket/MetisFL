# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metisfl/proto/learner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from metisfl.proto import model_pb2 as metisfl_dot_proto_dot_model__pb2
from metisfl.proto import service_common_pb2 as metisfl_dot_proto_dot_service__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bmetisfl/proto/learner.proto\x12\x07metisfl\x1a\x19metisfl/proto/model.proto\x1a\"metisfl/proto/service_common.proto\"{\n\x0cTrainRequest\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12$\n\x05model\x18\x02 \x01(\x0b\x32\x0e.metisfl.ModelR\x05model\x12,\n\x06params\x18\x03 \x01(\x0b\x32\x14.metisfl.TrainParamsR\x06params\"\xb5\x01\n\x0bTrainParams\x12)\n\x10global_iteration\x18\x01 \x01(\rR\x0fglobalIteration\x12\x1d\n\nbatch_size\x18\x02 \x01(\rR\tbatchSize\x12\x16\n\x06\x65pochs\x18\x03 \x01(\rR\x06\x65pochs\x12*\n\x11num_local_updates\x18\x04 \x01(\rR\x0fnumLocalUpdates\x12\x18\n\x07metrics\x18\x05 \x03(\tR\x07metrics\"}\n\x0f\x45valuateRequest\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12$\n\x05model\x18\x02 \x01(\x0b\x32\x0e.metisfl.ModelR\x05model\x12+\n\x06params\x18\x03 \x01(\x0b\x32\x13.metisfl.EvalParamsR\x06params\"E\n\nEvalParams\x12\x1d\n\nbatch_size\x18\x01 \x01(\rR\tbatchSize\x12\x18\n\x07metrics\x18\x02 \x03(\tR\x07metrics\"\xc2\x01\n\x10\x45valuateResponse\x12\x17\n\x07task_id\x18\x01 \x01(\tR\x06taskId\x12S\n\x0emetrics_values\x18\x02 \x03(\x0b\x32,.metisfl.EvaluateResponse.MetricsValuesEntryR\rmetricsValues\x1a@\n\x12MetricsValuesEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x02R\x05value:\x02\x38\x01\x32\xc5\x02\n\x0eLearnerService\x12\x31\n\x0fGetHealthStatus\x12\x0e.metisfl.Empty\x1a\x0c.metisfl.Ack\"\x00\x12,\n\x08GetModel\x12\x0e.metisfl.Empty\x1a\x0e.metisfl.Model\"\x00\x12\x33\n\x11SetInitialWeights\x12\x0e.metisfl.Model\x1a\x0c.metisfl.Ack\"\x00\x12.\n\x05Train\x12\x15.metisfl.TrainRequest\x1a\x0c.metisfl.Ack\"\x00\x12\x41\n\x08\x45valuate\x12\x18.metisfl.EvaluateRequest\x1a\x19.metisfl.EvaluateResponse\"\x00\x12*\n\x08ShutDown\x12\x0e.metisfl.Empty\x1a\x0c.metisfl.Ack\"\x00\x62\x06proto3')



_TRAINREQUEST = DESCRIPTOR.message_types_by_name['TrainRequest']
_TRAINPARAMS = DESCRIPTOR.message_types_by_name['TrainParams']
_EVALUATEREQUEST = DESCRIPTOR.message_types_by_name['EvaluateRequest']
_EVALPARAMS = DESCRIPTOR.message_types_by_name['EvalParams']
_EVALUATERESPONSE = DESCRIPTOR.message_types_by_name['EvaluateResponse']
_EVALUATERESPONSE_METRICSVALUESENTRY = _EVALUATERESPONSE.nested_types_by_name['MetricsValuesEntry']
TrainRequest = _reflection.GeneratedProtocolMessageType('TrainRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRAINREQUEST,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.TrainRequest)
  })
_sym_db.RegisterMessage(TrainRequest)

TrainParams = _reflection.GeneratedProtocolMessageType('TrainParams', (_message.Message,), {
  'DESCRIPTOR' : _TRAINPARAMS,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.TrainParams)
  })
_sym_db.RegisterMessage(TrainParams)

EvaluateRequest = _reflection.GeneratedProtocolMessageType('EvaluateRequest', (_message.Message,), {
  'DESCRIPTOR' : _EVALUATEREQUEST,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.EvaluateRequest)
  })
_sym_db.RegisterMessage(EvaluateRequest)

EvalParams = _reflection.GeneratedProtocolMessageType('EvalParams', (_message.Message,), {
  'DESCRIPTOR' : _EVALPARAMS,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.EvalParams)
  })
_sym_db.RegisterMessage(EvalParams)

EvaluateResponse = _reflection.GeneratedProtocolMessageType('EvaluateResponse', (_message.Message,), {

  'MetricsValuesEntry' : _reflection.GeneratedProtocolMessageType('MetricsValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _EVALUATERESPONSE_METRICSVALUESENTRY,
    '__module__' : 'metisfl.proto.learner_pb2'
    # @@protoc_insertion_point(class_scope:metisfl.EvaluateResponse.MetricsValuesEntry)
    })
  ,
  'DESCRIPTOR' : _EVALUATERESPONSE,
  '__module__' : 'metisfl.proto.learner_pb2'
  # @@protoc_insertion_point(class_scope:metisfl.EvaluateResponse)
  })
_sym_db.RegisterMessage(EvaluateResponse)
_sym_db.RegisterMessage(EvaluateResponse.MetricsValuesEntry)

_LEARNERSERVICE = DESCRIPTOR.services_by_name['LearnerService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EVALUATERESPONSE_METRICSVALUESENTRY._options = None
  _EVALUATERESPONSE_METRICSVALUESENTRY._serialized_options = b'8\001'
  _TRAINREQUEST._serialized_start=103
  _TRAINREQUEST._serialized_end=226
  _TRAINPARAMS._serialized_start=229
  _TRAINPARAMS._serialized_end=410
  _EVALUATEREQUEST._serialized_start=412
  _EVALUATEREQUEST._serialized_end=537
  _EVALPARAMS._serialized_start=539
  _EVALPARAMS._serialized_end=608
  _EVALUATERESPONSE._serialized_start=611
  _EVALUATERESPONSE._serialized_end=805
  _EVALUATERESPONSE_METRICSVALUESENTRY._serialized_start=741
  _EVALUATERESPONSE_METRICSVALUESENTRY._serialized_end=805
  _LEARNERSERVICE._serialized_start=808
  _LEARNERSERVICE._serialized_end=1133
# @@protoc_insertion_point(module_scope)
