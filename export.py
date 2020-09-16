from collections import defaultdict
import csv
import sys

import plyvel
import eth2spec.phase0.spec as spec

# See https://github.com/sigp/lighthouse/blob/ce10db15da0db4cbe76b96b58ccd1b40e39ed124/beacon_node/store/src/lib.rs#L195-L215
BLOCK_PREFIX = b"blk"

STEP_SIZE = 100

BLOCK_COLS = ['state_root', 'slot', 'proposer_index']


def extract_block_row(sbb: spec.SignedBeaconBlock):
    return (sbb.message.state_root, sbb.message.slot, sbb.message.proposer_index)


ATTESTATION_COLS = [
    'slot',
    'beacon_block_root',
    'attesting_indices',
    'source_epoch',
    'source_block_root',
    'target_epoch',
    'target_block_root',
]


def bitlist_to_str(bitlist: spec.Bitlist):
    length = bitlist.length()
    return ''.join('1' if bitlist.get(i) else '0' for i in range(length))


def extract_attestation_rows(sbb: spec.SignedBeaconBlock):
    attestations = sbb.message.body.attestations

    return [(
        sbb.message.slot,
        a.data.beacon_block_root,
        bitlist_to_str(a.aggregation_bits),
        a.data.source.epoch,
        a.data.source.root,
        a.data.target.epoch,
        a.data.target.root
    ) for a in attestations]


def export_blocks(lighthouse_dir, out_dir):
    db_dir = f"{lighthouse_dir}/beacon/chain_db"
    db = plyvel.DB(db_dir)

    blocks = []
    attestations = []

    try:
        count = 0
        for key, value in db:
            if key[:3] == BLOCK_PREFIX:
                signed_beacon_block = spec.SignedBeaconBlock.decode_bytes(value)

                blocks.append(extract_block_row(signed_beacon_block))
                attestations.extend(extract_attestation_rows(signed_beacon_block))

                if count > 0 and count % STEP_SIZE == 0:
                    print(f'{count} blocks processed')

                    block_file = f"{out_dir}/blocks_{count // STEP_SIZE}.csv"
                    with open(block_file, 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(BLOCK_COLS)
                        for block in blocks:
                            writer.writerow(block)
                    blocks = []

                    attestation_file = f"{out_dir}/attestations_{count // STEP_SIZE}.csv"
                    with open(attestation_file, 'w') as f:
                        writer = csv.writer(f)
                        writer.writerow(ATTESTATION_COLS)
                        for attestation in attestations:
                            writer.writerow(attestation)
                    attestations = []

                count += 1

        return blocks

    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: `python export.py $LIGHTHOUSE_DIR $OUTPUT_DIR`')

    else:
        lighthouse_dir = sys.argv[1]
        out_dir = sys.argv[2]
        export_blocks(lighthouse_dir, out_dir)
