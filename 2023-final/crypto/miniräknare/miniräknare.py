class Calculator:
    def __init__(self):
        self.allowed = "0123456789C%/*-+=.<"
        self.state = ""
    
    def eval(self):
        for press in self.state:
            assert press in self.allowed
        
        self.set_state(self.state.replace("C", "*0")) # clear
        self.set_state(self.state.replace("%", " // 100 * ")) # percentage

        return eval(self.state)

    def press_buttons(self, buttons):
        for button in buttons:
            self.press_button(button)

    def press_button(self, button):
        assert len(button) == 1

        if button == "=":
            return self.set_state(self.eval())
        
        self.state += button
    
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = str(state)
        return self.get_state()