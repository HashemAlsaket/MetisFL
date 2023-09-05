
import signal
from typing import Optional

from metisfl.common.types import ClientParams, LearnerConfig, ServerParams
from metisfl.learner.controller_client import GRPCClient
from metisfl.learner.learner import Learner, has_all
from metisfl.learner.learner_server import LearnerServer
from metisfl.learner.message_helper import MessageHelper
from metisfl.learner.task_manager import TaskManager
from metisfl.encryption import HomomorphicEncryption


def register_handlers(client: GRPCClient, server: LearnerServer):
    """ Register handlers for SIGTERM and SIGINT to leave the federation.

    Parameters
    ----------
    client : GRPCClient
        The GRPCClient object.
    server : LearnerServer
        The LearnerServer object.
    """

    def handler(signum, frame):
        print("Received SIGTERM, leaving federation...")
        client.leave_federation(block=False, request_timeout=1)
        client.shutdown_client()
        server.ShutDown(None, None)
        exit(0)

    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)


def validate_learner(learner: Learner) -> bool:
    """Returns True if the given learner has all methods, False otherwise."""

    if not has_all(learner):
        raise ValueError(
            "Learner must have get_weights, set_weights, train, and evaluate methods"
        )


def app(
    learner: Learner,
    client_params: ClientParams,
    server_params: ServerParams,
    learner_config: Optional[LearnerConfig] = None,
):
    """Entry point for the MetisFL Learner application.

    Parameters
    ----------
    learner : Learner
        The Learner object. Must impliment the Learner interface.
    client_params : ClientParams
        The client parameters of the Learner client. 
    server_params : ServerParams
        The server parameters of the Learner server. 
    learner_config : Optional[LearnerConfig], (default=None)
        The configuration of the Learner containing the Homomorphic Encryption scheme. 
    """

    # Sanity check the learner
    validate_learner(learner)

    # Setup the Homomorphic Encryption scheme if provided
    enc = None
    if learner_config:
        enc = HomomorphicEncryption(
            batch_size=learner_config.batch_size,
            scaling_factor_bits=learner_config.scaling_factor_bits,
            crypto_context_path=learner_config.crypto_context,
            public_key_path=learner_config.public_key,
            private_key_path=learner_config.private_key,
        )

    # Create the MessageHelper
    message_helper = MessageHelper(scheme=enc)

    # Create the gRPC client to communicate with the Controller
    client = GRPCClient(
        client_params=client_params,
        message_helper=message_helper,
    )

    # Create the gRPC server for the Controller to communicate with the Learner
    server = LearnerServer(
        learner=learner,
        server_params=server_params,
        task_manager=TaskManager(),
        client=client,
        message_helper=message_helper,
    )

    # Register with the Controller
    client.join_federation(client_params=ClientParams(
        hostname=server_params.hostname,
        port=server_params.port,
        root_certificate=server_params.root_certificate,
    ))

    # Register handlers
    register_handlers(client, server)

    # Start the Learner server; blocking call
    server.start()
