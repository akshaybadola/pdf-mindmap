from typing import Optional
import os

from PyQt5.QtWidgets import QGraphicsScene

from .mmap import MMap
from .watcher import Watcher
from .util import PathLike


class Scene(QGraphicsScene):
    """A scene to hold a mindmap. Scene is separate from the mindmap
    so that a new mindmap can be placed on to it easily if required.

    """

    def __init__(self, root_dir: Optional[PathLike] = None,
                 store_dir: Optional[PathLike] = None,
                 filename: Optional[PathLike] = None):
        """Initialize the MindMap Scene

        Args:
            root_dir: Root directory for PDF files
            store_dir: Root directory to store the mindmap state
            filename: Filename to load

        """
        super().__init__()
        self.root_dir = root_dir
        self.store_dir = store_dir
        self.filename = filename
        # Create a new watcher instance which should actually be for each Sheet
        if self.root_dir:
            self.watcher = Watcher(self.root_dir, self.store_dir)
        self.create_new_map()
        self.monitor()
        self.hashes = {}

    def monitor(self):
        if self.root_dir:
            pdfs, added = self.watcher.check()
            if added:
                self.files_hashes = self.watcher.proc_data[0]  # file -> (hash, metadata)
                self.hashes_files = self.watcher.proc_data[1]  # hash -> (file, metadata)
            new_hashes = set(self.hashes_files.keys())

    def exit_app(self):
        # check if saving
        # if not:
        pass

    def create_new_map(self):
        if self.root_dir:
            self.create_tree()
            self.mmap = MMap(self, dirtree=self.thought_tree)
        elif self.filename:
            self.mmap = MMap(self, filename=self.filename)
        else:
            self.mmap = MMap(self)

    def create_tree(self):
        self.files = []
        self.thought_tree = {}
        for root, dirs, files_ in os.walk(self.root_dir, topdown=True):
            self.files.append((root, [f for f in files_ if '.pdf' in f]))
        self.gen_tree()

    def gen_tree(self):
        # gen_tree I think is independent of everything else
        index = 0
        root_index = index
        root_thought = self.files[root_index]
        self.thought_tree[0] = {'index': index, 'name': root_thought[0],
                                'parent': None, 'children': [], 'files': root_thought[1]}

        while root_index < len(self.files):
            root_thought = (self.thought_tree[root_index]['name'], self.thought_tree[root_index]['files'])
            for f in self.files:
                if os.path.dirname(f[0]) == root_thought[0]:
                    index += 1
                    self.thought_tree[index] = {'index': index, 'name': f[0],
                                                'parent': root_index, 'children': [], 'files': f[1]}
                    self.thought_tree[root_index]['children'].append(index)
            root_index += 1
