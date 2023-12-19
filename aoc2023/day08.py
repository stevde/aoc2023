from __future__ import annotations
from dataclasses import dataclass, field
import logging
import math
import re
from typing import Iterable

logger = logging.getLogger()


@dataclass
class Node:
    name: str
    left: Node = None
    right: Node = None


@dataclass
class Instructions:
    directions: str = None
    nodes: dict[str, Node] = field(default_factory=dict)

    def get_or_create(self, node_name: str) -> Node:
        if node_name in self.nodes:
            return self.nodes[node_name]

        node = Node(node_name)
        self.nodes[node_name] = node
        return node


RE_NODE = re.compile(r"[A-Z]{3}")


def parse_input(lines: Iterable[str]) -> Instructions:
    instructions = Instructions()

    for i, line in enumerate(lines):
        if i == 0:
            instructions.directions = line
        elif i > 1:
            match = RE_NODE.findall(line)
            node_name, left_name, right_name = match[0], match[1], match[2]

            node = instructions.get_or_create(node_name)
            left = instructions.get_or_create(left_name)
            right = instructions.get_or_create(right_name)

            node.left = left
            node.right = right

    return instructions


def part_one(lines: Iterable[str]) -> int:
    instructions = parse_input(lines)
    node = instructions.nodes["AAA"]

    i = 0
    while node != instructions.nodes["ZZZ"]:
        direction = instructions.directions[i % len(instructions.directions)]
        if direction == "R":
            node = node.right
        if direction == "L":
            node = node.left
        i += 1

    return i


def detect_loop(node: Node, instructions: Instructions) -> int:
    i = 0
    while not (node.name.endswith("Z")):
        direction = instructions.directions[i % len(instructions.directions)]
        if direction == "R":
            node = node.right
        if direction == "L":
            node = node.left
        i += 1
    return i


def part_two(lines: Iterable[str]) -> int:
    instructions = parse_input(lines)
    start_nodes = [
        node for name, node in instructions.nodes.items() if name.endswith("A")
    ]
    loops = [detect_loop(node, instructions) for node in start_nodes]
    logger.debug(loops)


    return math.lcm(*loops)
