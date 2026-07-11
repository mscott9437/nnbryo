import hashlib
import time

import numpy as np
import torch

# --------------------------------------------------
# Runtime Metadata
# --------------------------------------------------

RUNTIME_NAME = "NNBryo"
RUNTIME_VERSION = "0.14"

# --------------------------------------------------
# Identity
# --------------------------------------------------

ldap_identity = (
    "uid=alice,"
    "ou=admins,"
    "dc=example,"
    "dc=com"
)

identity_hash = hashlib.sha256(
    ldap_identity.encode()
).digest()

identity_affinity = identity_hash[0] / 255.0

# --------------------------------------------------
# Semantic Runtime Device
# --------------------------------------------------

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print(f"{RUNTIME_NAME} {RUNTIME_VERSION}")
print(f"Semantic Runtime Device: {device}")

# --------------------------------------------------
# Runtime Tensor Layout
# --------------------------------------------------

AFFINITY     = 0
CONTINUITY   = 1
DECAY        = 2
DRIFT        = 3
TRAJECTORY   = 4
TRUST        = 5
PRIVILEGE    = 6
AUTHORIZED   = 7
TICK         = 8
UPTIME       = 9

runtime_state = torch.zeros(
    10,
    dtype=torch.float32,
    device=device
)

# --------------------------------------------------
# Runtime State
# --------------------------------------------------

trust = {
    "identity": ldap_identity,
    "affinity": identity_affinity,
    "continuity": 1.0,
    "decay": 1.0,
    "drift": 0.05,
    "trajectory": 0.0,
    "privilege": 1.5,
    "trust": 1.0,
    "authorized": True,
}

TRUST_THRESHOLD = 0.50

DECAY_RATE = 0.02
UPDATE_RATE = 100.0

tick = 0
uptime = 0.0

previous_trust = trust["trust"]
previous_update = time.perf_counter()

# --------------------------------------------------
# Publish Semantic Runtime State
# --------------------------------------------------

def publish_runtime_state():

    runtime_state.copy_(torch.tensor([
        trust["affinity"],
        trust["continuity"],
        trust["decay"],
        trust["drift"],
        trust["trajectory"],
        trust["trust"],
        trust["privilege"],
        float(trust["authorized"]),
        float(tick),
        uptime
    ],
    dtype=torch.float32,
    device=device))

# Publish initial snapshot
publish_runtime_state()

# --------------------------------------------------
# Continuous Trust Runtime
# --------------------------------------------------

while True:

    #
    # Acquire timing
    #

    now = time.perf_counter()
    dt = now - previous_update
    previous_update = now

    tick += 1
    uptime += dt

    #
    # Continuous Trust Decay
    #

    trust["decay"] *= np.exp(
        -DECAY_RATE * dt
    )

    #
    # Trust Evolution
    #

    trust["trust"] = (
        trust["continuity"]
        * trust["affinity"]
        * trust["decay"]
    )

    #
    # Drift
    #

    trust["trust"] -= trust["drift"]

    #
    # Privilege
    #

    trust["trust"] /= trust["privilege"]

    #
    # Clamp
    #

    trust["trust"] = np.clip(
        trust["trust"],
        0.0,
        1.0
    )

    #
    # Trajectory
    #

    trust["trajectory"] = (
        trust["trust"]
        - previous_trust
    )

    previous_trust = trust["trust"]

    #
    # Authorization
    #

    trust["authorized"] = (
        trust["trust"]
        >= TRUST_THRESHOLD
    )

    #
    # Publish semantic runtime snapshot
    #

    publish_runtime_state()

    #
    # Telemetry
    #

    print(
        f"tick={tick:06d} "
        f"trust={trust['trust']:.4f} "
        f"trajectory={trust['trajectory']:.6f} "
        f"decay={trust['decay']:.4f} "
        f"authorized={trust['authorized']}"
    )

    #
    # Future:
    #
    # Semantic events from OCaml
    #
    # trust["continuity"] += ...
    # trust["drift"] += ...
    # trust["trust"] += ...
    #
    # Future:
    #
    # TCP Authorization
    #
    # authorize(runtime_state.clone())
    #

    time.sleep(
        1.0 / UPDATE_RATE
    )
