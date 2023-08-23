# An attempt at a MindMap library in PyQt5

**This is unmaintained and very buggy**

See [citemap](https://github.com/akshaybadola/citemap) for the **new library**.


## History

This was an early attempt at building a MindMap for PDF files.
I was facing issues linking the various research papers I was going through.
Notes were separate from files, references and citing papers were in separate
directories and it was hard to keep track. This had options to attach and
I think I had written separate PDF metadata parsing functions in a separate
library. That was also abandoned.

Ultimately I built [ref-man](https://github.com/akshaybadola/ref-man) for
[Emacs](https://www.gnu.org/s/emacs/) and [org-mode](https://orgmode.org/)
which had all the functionality I required except for citation visualization.

I'll see if I can quickly integrate the components from this library
into a separate library to visualize the citation network. Current tools
aren't adequate to do so as they are either not free or aren't interactive.


