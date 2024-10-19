"""
Recursively update all branches in the project to be rebased on each other.
This is done to ease the process of adding new things to the base or interim setups,
without having to manually go to each branch and rebase it after applying update to it's ancestor.
"""

import subprocess
from dataclasses import dataclass


def run(command: str | list[str]):
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode().strip()


CORNER_BRANCHES = [
    "drf/docker/django",
]


@dataclass
class Branch:
    name: str

    @property
    def parent(self) -> "Branch | None":
        if self.name == "master":
            return None
        try:
            _, parent_name = self.name.split("/", maxsplit=1)
        except ValueError:  # Current branch is direct child of master branch.
            return Branch(name="master")

        return Branch(name=parent_name)

    @property
    def ancestors(self):
        parent = self.parent
        result = []
        while parent is not None:
            result.append(parent)
            parent = parent.parent
        return result

    def __str__(self):
        return self.name


@dataclass
class Git:
    @property
    def current_branch(self):
        return Branch(name=run("git branch --show-current"))

    def checkout(self, to: Branch):
        run(f"git checkout {to}")
        return self

    def rebase(self, from_: Branch | None, on: Branch):
        if from_:
            self.checkout(to=from_)

        run(f"git pull --rebase origin {on}")
        return self

    def push(self):
        run("git push --force-with-lease")
        return self


if __name__ == "__main__":
    git = Git()
    for branch_name in CORNER_BRANCHES:
        corner_branch = Branch(branch_name)
        for branch in reversed(corner_branch.ancestors[:-1]):
            git.rebase(branch, branch.parent).push()

        git.rebase(corner_branch, corner_branch.parent).push()
