from collections import defaultdict

import plyvel
import eth2spec.phase0.spec as spec

# See https://github.com/sigp/lighthouse/blob/ce10db15da0db4cbe76b96b58ccd1b40e39ed124/beacon_node/store/src/lib.rs#L195-L215
BLOCK_PREFIX = b"blk"


def export_blocks(lighthouse_dir):
    db_dir = f"{lighthouse_dir}/beacon/chain_db"
    db = plyvel.DB(db_dir)

    blocks = []
    for key, value in db:
        if key[:3] == BLOCK_PREFIX:
            block = spec.SignedBeaconBlock.decode_bytes(value)
            blocks.append(block)

    return blocks


# TODO: don't hardcode my own path in here
if __name__ == "__main__":
    blocks = export_blocks("/Users/lakshmansankar/.lighthouse")
    print(blocks)
