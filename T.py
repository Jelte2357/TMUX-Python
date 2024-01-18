from __future__ import annotations

from typing import TYPE_CHECKING

from textual import events
from textual.app import App
from textual.reactive import Reactive
import os
from tinp import TextInput
import subprocess
from configparser import ConfigParser
if TYPE_CHECKING:
    from textual.message import Message

os.system('title TMUX in python')



class SimpleForm(App):

    current_index: Reactive[int] = Reactive(-1)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tab_index = ["codeL", "codeR"]

    async def on_load(self) -> None:
        await self.bind("enter", "submit")
        await self.bind("ctrl+b", "next_tab_index")

    async def on_mount(self) -> None:
        try:
            config = ConfigParser()
            config.read('TMUX.ini')
            self.colorL = config['COLORS']['colorL']
            self.colorR = config['COLORS']['colorR']
        except:
            self.colorL = 'white'
            self.colorR = 'white'
        
        self.codeL = TextInput(
            name="codeL",
            placeholder="",
            value=os.getcwd() + "> ",
            #title=os.getcwd() + ">",
            color=self.colorL,
        )
        
        self.codeR = TextInput(
            name="codeR",
            placeholder="",
            value=os.getcwd() + "> ",
            #title=os.getcwd() + ">",
            color=self.colorR,
        )
        

        #await self.view.dock(self.output, edge="left", size=40)
        await self.view.dock(
            self.codeL, edge="left", size=0
        )
        await self.view.dock(
            self.codeR, edge="right", size=0
        )
        
        # change the size of codeL
        w, _ = os.get_terminal_size()
        self.codeL.layout_size = w - w // 2
        self.codeR.layout_size = w // 2
        # change the title of codeL
        #self.codeL.title = 
        
        await self.codeL.focus()

    async def action_next_tab_index(self) -> None:
        await getattr(self, self.tab_index[1 - self.current_index]).focus()
    
    async def action_submit(self) -> None:
        # get the last value of the selected field (so the last one split by \n)
        # put it after the text "Field Contains: "
        await self.run_command()
        #("\n" if '> '.join(value.split("> ")[1:]).split() else "")   
        getattr(self, self.tab_index[self.current_index])._cursor_position = len(getattr(self, self.tab_index[self.current_index]).value)

    async def handle_input_on_focus(self, message: Message) -> None:
        self.current_index = self.tab_index.index(message.sender.name)
        
    async def on_resize(self, event: events.Resize) -> None:
        w, _ = os.get_terminal_size()
        self.codeL.layout_size = w - w // 2
        self.codeR.layout_size = w // 2
        return await super().on_resize(event)
    
    async def run_command(self) -> None:
        side = getattr(self, self.tab_index[self.current_index])
        command = '> '.join(side.value.split('\n')[-1].split('> ')[1:])
        # clear the side on clear command
        if command == 'clear':
           side.value = f"{os.getcwd()}> "
           return

        side.value += f"\n{os.getcwd()}> "        
    
        
        



if __name__ == "__main__":
    SimpleForm.run(title="Textual-Inputs Simple Form")
