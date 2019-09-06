from tkinter import Frame


class dFrame(Frame):
    def enable(self, state='!disabled'):
        def cstate(widget):
            # Is this widget a container?
            if widget.winfo_children:
                # It's a container, so iterate through its children
                for w in widget.winfo_children():
                    # change its state
                    w.state((state,))
                    # and then recurse to process ITS children
                    cstate(w)

            cstate(self)

    def disable(self):
        self.enable('disabled')