import yaml

from metisfl import config
from metisfl.proto import metis_pb2

from metisfl.proto import metis_pb2
from metisfl.proto.proto_messages_factory import MetisProtoMessages
from .fedenv_schema import env_schema


class FederationEnvironment(object):

    def __init__(self, federation_environment_config_fp):
        fstream = open(federation_environment_config_fp).read()
        self._yaml = yaml.load(fstream, Loader=yaml.SafeLoader)
        env_schema.validate(self._yaml)
        ssl_public_certificate, ssl_private_key = self._setup_ssl()
        self._setup_fhe()
        self.controller = RemoteHost(self._yaml.get("Controller"),
                                     ssl_public_certificate=ssl_public_certificate,
                                     ssl_private_key=ssl_private_key)
        self.learners = [RemoteHost(learner,
                                    ssl_public_certificate=ssl_public_certificate,
                                    ssl_private_key=ssl_private_key) for learner in self._yaml.get("Learners")]

    def _setup_ssl(self):
        ssl_public_certificate, ssl_private_key = None, None
        if self.enable_ssl:
            ssl_public_certificate = self._yaml.get("SSLPublicCertificate")
            ssl_private_key = self._yaml.get("SSLPrivateKey")
            if not ssl_public_certificate and not ssl_private_key:
                ssl_public_certificate, ssl_private_key = config.get_certificates()
            elif ssl_public_certificate and ssl_private_key:
                return
            else:
                raise ValueError(
                    "Both SSL public certificate and private key must be provided.")
        return ssl_public_certificate, ssl_private_key

    def _setup_fhe(self):
        if self._yaml.get("HEScheme") == "CKKS":
            fhe_crypto_context_file, fhe_key_public_file, \
                fhe_key_private_file, fhe_key_eval_mult_file = config.get_fhe_resources()
            self._yaml["FHECryptoContextFile"] = fhe_crypto_context_file
            self._yaml["FHEPublicKeyFile"] = fhe_key_public_file
            self._yaml["FHEPrivateKeyFile"] = fhe_key_private_file
            self._yaml["FHEKeyEvalMultFile"] = fhe_key_eval_mult_file

    # Environment configuration
    @property
    def federation_rounds(self):
        return self._yaml.get("FederationRounds")

    @property
    def execution_time_cutoff_mins(self):
        return self._yaml.get("ExecutionCutoffTimeMins")

    @property
    def evaluation_metric(self):
        return self._yaml.get("EvaluationMetric")
    
    @property
    def metric_cutoff_score(self):
        return self._yaml.get("EvaluationMetricCutoffScore")

    @property
    def communication_protocol(self):
        return self._yaml.get("CommunicationProtocol")

    @property
    def enable_ssl(self):
        return self._yaml.get("EnableSSL", False)

    @property
    def model_store(self):
        return self._yaml.get("ModelStore", "InMemory")

    @property
    def model_store_hostname(self):
        return self._yaml.get("ModelStoreHostname", None)

    @property
    def model_store_port(self):
        return self._yaml.get("ModelStorePort", None)

    @property
    def eviction_policy(self):
        return self._yaml.get("EvictionPolicy", "LineageLengthEviction")

    @property
    def lineage_length(self):
        return self._yaml.get("LineageLength", 1)

    def get_local_model_config_pb(self):
        return MetisProtoMessages.construct_controller_modelhyperparams_pb(
            batch_size=self._yaml.get("BatchSize"),
            epochs=self._yaml.get("LocalEpochs"))

    def get_global_model_config_pb(self):
        aggregation_rule_pb = MetisProtoMessages.construct_aggregation_rule_pb(
            rule_name=self._yaml.get("AggregationRule"),
            scaling_factor=self._yaml.get("ScalingFactor"),
            stride_length=self._yaml.get("StrideLength"),
            he_scheme_config_pb=self.get_he_scheme_pb(entity="controller"))
        return MetisProtoMessages.construct_global_model_specs(
            aggregation_rule_pb=aggregation_rule_pb)

    def get_he_scheme_pb(self, entity: str) -> metis_pb2.HESchemeConfig:
        assert entity in ["controller", "learner"]
        if self._yaml.get("HEScheme") == "CKKS":
            fhe_crypto_context_file = self._yaml["FHECryptoContextFile"]
            fhe_key_public_file = self._yaml["FHEPublicKeyFile"]
            fhe_key_private_file = self._yaml["FHEPrivateKeyFile"]
            ckks_scheme_pb = metis_pb2.CKKSSchemeConfig(
                batch_size=self._yaml.get("HEBatchSize"),
                scaling_factor_bits=self._yaml.get("HEScalingBits")
            )
            return metis_pb2.HESchemeConfig(
                enabled=True,
                crypto_context_file=fhe_crypto_context_file,
                public_key_file=fhe_key_public_file if entity == "learner" else None,
                private_key_file=fhe_key_private_file if entity == "learner" else None,
                ckks_scheme_config=ckks_scheme_pb)
        else:
            empty_scheme_pb = metis_pb2.EmptySchemeConfig()
            return metis_pb2.HESchemeConfig(enabled=False,
                                            empty_scheme_config=empty_scheme_pb)

    def get_communication_protocol_pb(self):
        # @stripeli clarify this
        protocol = self._yaml.get("CommunicationProtocol")
        semi_synchronous_lambda, semi_sync_recompute_num_updates = None, None
        if protocol == "SemiSynchronous":
            semi_synchronous_lambda = self._yaml.get(
                "SemiSynchronousLambda")
            semi_sync_recompute_num_updates = self._yaml.get(
                "SemiSynchronousRecomputeSteps")

        return MetisProtoMessages.construct_communication_specs_pb(
            protocol=self.communication_protocol,
            semi_sync_lambda=semi_synchronous_lambda,
            semi_sync_recompute_num_updates=semi_sync_recompute_num_updates)

    def get_model_store_config_pb(self):
        model_store = self._yaml.get("ModelStore", "InMemory")
        eviction_policy = self._yaml.get("EvictionPolicy", "LineageLengthEviction")
        eviction_policy_pb = MetisProtoMessages.construct_eviction_policy_pb(
            self.eviction_policy, self.lineage_length)
        model_store_specs_pb = MetisProtoMessages.construct_model_store_specs_pb(
            eviction_policy_pb)
        if self.model_store.upper() == "INMEMORY":
            model_store_pb = metis_pb2.InMemoryStore(
                model_store_specs=model_store_specs_pb)
            return metis_pb2.ModelStoreConfig(in_memory_store=model_store_pb)
        elif self.model_store.upper() == "REDIS":
            model_store_hostname = self._yaml.get("ModelStoreHostname")
            model_store_port = self._yaml.get("ModelStorePort")
            server_entity_pb = MetisProtoMessages.construct_server_entity_pb(hostname=model_store_hostname,
                                                                             port=model_store_port)
            return metis_pb2.RedisDBStore(model_store_specs=model_store_specs_pb,
                                          server_entity=server_entity_pb)
        else:
            raise RuntimeError("Not a supported model store.")


class RemoteHost(object):
    def __init__(self, config_map, ssl_public_certificate=None, ssl_private_key=None):
        self._config_map = config_map
        self._ssl_public_certificate = ssl_public_certificate
        self._ssl_private_key = ssl_private_key

    @property
    def id(self):
        return "{}:{}".format(self.grpc_hostname, self.grpc_port)

    @property
    def project_home(self):
        return self._config_map.get("ProjectHome")

    @property
    def hostname(self):
        return self._config_map.get("Hostname")

    @property
    def cuda_devices(self):
        return self._config_map.get("CudaDevices", None)

    @property
    def port(self):
        return self._config_map.get("Port", None)

    @property
    def username(self):
        return self._config_map.get("Username")

    @property
    def password(self):
        return self._config_map.get("Password")

    @property
    def key_filename(self):
        return self._config_map.get("KeyFilename")

    @property
    def passphrase(self):
        return self._config_map.get("Passphrase")

    @property
    def on_login_command(self):
        return self._config_map.get("OnLoginCommand")

    @property
    def grpc_hostname(self):
        return self._config_map.get("GRPCServicerHostname")

    @property
    def grpc_port(self):
        return self._config_map.get("GRPCServicerPort")

    @property
    def ssl_private_key(self):
        return self._config_map.get("SSLPrivateKey")

    @property
    def ssl_public_certificate(self):
        return self._config_map.get("SSLPublicCertificate")

    def get_fabric_connection_config(self):
        # Look for parameters values here:
        # https://docs.paramiko.org/en/latest/api/client.html#paramiko.client.SSHClient.connect
        # 'allow_agent' show be disabled if working with username/password.
        connect_kwargs = {
            "password": self.password,
            "allow_agent": False if self.password else True,
            "look_for_keys": True if self.key_filename else False,
        }
        if self.key_filename:
            connect_kwargs["key_filename"] = self.key_filename
            connect_kwargs["passphrase"] = self.passphrase

        conn_config = {
            "host": self.hostname,
            "port": self.port,
            "user": self.username,
            "connect_kwargs": connect_kwargs
        }
        return conn_config

    # @stripeli: what does this param do?
    def get_server_entity_pb(self, gen_connection_entity=False) -> metis_pb2.ServerEntity:
        return metis_pb2.ServerEntity(
            hostname=self._config_map.get("GRPCServicerHostname"),
            port=self._config_map.get("GRPCServicerPort"),
            public_certificate_file=self._ssl_public_certificate,
            private_key_file=self._ssl_private_key if not gen_connection_entity else None,
        )
