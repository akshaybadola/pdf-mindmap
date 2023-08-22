import os
import sys
import argparse
import configparser
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGraphicsView, QApplication, QMainWindow, QGraphicsScene,
                             QStatusBar, QGridLayout, QAction)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtOpenGL import QGL, QGLWidget, QGLFormat

from docmind import Scene, LineEdit, StatusBar, View


class AppWindow(QMainWindow):
    def __init__(self, view, title):
        super().__init__()
        self._view = view
        self._title = title
        self._actions = {}
        self.initUI(view)

    def _add_action(self, name, key_seq, func):
        self._actions[name] = QAction(name, self)
        self._actions[name].setShortcut(key_seq)
        self._actions[name].triggered.connect(func)
        self.addAction(self._actions[name])

    def initUI(self, view):
        self.setCentralWidget(view)

        self._add_action("Zoom in", "Ctrl++", self.zoom_in)
        self._add_action("Zoom out", "Ctrl+-", self.zoom_out)
        self._add_action("Save File", "Ctrl+x,Ctrl+c", self.save_file)

        self.setWindowTitle(self._title)
        self.setGeometry(100, 100, 1200, 800)

    def zoom_in(self):
        # Add code here to zoom in your QGraphicsView
        print('Zoom In')

    def zoom_out(self):
        # Add code here to zoom out your QGraphicsView
        print('Zoom Out')

    def save_file(self):
        # Add code here to zoom out your QGraphicsView
        print('Saving File')

    def abort(self):
        # pass abort to children
        pass

    def quit(self):
        # Quit the window
        pass


def create_view(root_dir, store_dir, filename):
    """Create the :class:`QGraphicsView` view that'll hold the mind maps

    Args:
        root_dir: Root directory to monitor pdf files
        store_dir: Application store directory
        filename: Optional filename to open

    """
    scene = Scene(root_dir=root_dir, store_dir=store_dir, filename=filename)
    view = View(scene, scene.mmap)
    view.setCacheMode(view.CacheBackground)
    view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
    view.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
    view.resize(1200, 800)
    line_edit = LineEdit(view)
    status_bar = QStatusBar(view)
    scene.mmap.init_widgets(line_edit, status_bar)
    # view.horizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    # view.verticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    # mindmap.setSceneRect(0, 0, 1200, 800)
    scene.stickyFocus = True
    view.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
    # view.show()
    return view


def main():
    default_config_dir = Path.joinpath(Path.home().absolute(), ".mindmap")
    parser = argparse.ArgumentParser(description='Mindmap for documents')
    parser.add_argument("-c", "--config-dir", type=str,
                        default=str(default_config_dir),
                        help="Load this config file")
    parser.add_argument("--root-dir", "-r", type=str, default=str(default_config_dir.joinpath("pdfs")),
                        help="The root directory from where to monitor pdf files")
    parser.add_argument("--store-dir", "-s", type=str, default=str(default_config_dir.joinpath("store")),
                        help="Store the application data in this directory. Defaults to $HOME/.mindmap")
    parser.add_argument("--file", "-f", type=str, default="", help="Open this saved file")
    args = parser.parse_args()

    filename = None
    config_dir = Path(args.config_dir)
    store_dir = Path(args.store_dir)
    if os.path.exists(args.root_dir):
        print("Trying to populate the thought tree from root dir")
        root_dir = Path(args.root_dir)
    elif os.path.exists(args.file):
        print("Opening file: " + args.file)
        if os.path.exists(args.file):
            filename = Path(args.file)
    else:
        root_dir = None
        print("No root directory or file given. Creating empty sheet.")

    if not os.path.exists(config_dir):
        Path.mkdir(config_dir)
    if not os.path.exists(store_dir):
        Path.mkdir(store_dir)

    app = QApplication(sys.argv)
    # TODO: This view and mindmap should be initialized somewhere else
    view = create_view(root_dir, store_dir, filename)
    window = AppWindow(view, "Mind Map")
    window.show()
    # import ipdb; ipdb.set_trace()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
