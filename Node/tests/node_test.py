"I test the functionality provided by the node.py file."

from attrdict import AttrDict

from Node.files import node

LAS_SENT_BLOCK = AttrDict({'blockId': '0', 'difficulty': 2.0, 'timestamp': 1})
BLOCKS = [AttrDict({'blockId': '1', 'difficulty': 2.0, 'timestamp': 2}),
          AttrDict({'blockId': '2', 'difficulty': 3.0, 'timestamp': 3}),
          AttrDict({'blockId': '3', 'difficulty': 4.0, 'timestamp': 4})]


def test_avg_difficulty():
    assert node.calculate_avg_block_difficulty(BLOCKS) == 3


def test_avg_block_time():
    assert node.calculate_avg_block_time(BLOCKS, LAS_SENT_BLOCK) == 1


if __name__ == "__main__":
    test_avg_difficulty()
    test_avg_block_time()
