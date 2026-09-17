import adsk.core
import os
from ..lib import fusion360utils as futil
from .. import config
app = adsk.core.Application.get()
ui = app.userInterface


# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdBtn'
CMD_NAME = 'SketchVis'
CMD_Description = 'Toggle Display Settings | Object Visibility | Sketches'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# Set of known names and identifiers for 'Sketches' across supported languages in Fusion 360
SKETCH_NAMES = {
    # English
    'sketches', 'sketch',
    # German (Skizzen)
    'skizzen', 'skizze',
    # French (Esquisses)
    'esquisses', 'esquisse',
    # Spanish (Bocetos)
    'bocetos', 'boceto',
    # Italian (Schizzi)
    'schizzi', 'schizzo',
    # Japanese (スケッチ)
    'スケッチ',
    # Chinese Simplified (草图) & Traditional (草圖)
    '草图', '草圖',
    # Korean (스케치)
    '스케치',
    # Portuguese (Esboços)
    'esboços', 'esboço', 'esbocos', 'esboco',
    # Russian (Эскизы)
    'эскизы', 'эскиз',
    # Polish (Szkice)
    'szkice', 'szkic',
    # Turkish (Çizimler)
    'çizimler', 'çizim', 'cizimler', 'cizim',
    # Czech (Náčrty)
    'náčrty', 'náčrt', 'nacrty', 'nacrt',
}


def get_sketch_item_index(list_items) -> int:
    """
    Searches through the listItems collection of VisibilityOverrideCommand to locate
    the index (offset) of the 'Sketches' item dynamically.
    
    Checks both 'name' and 'id' properties against 'Sketches' as well as known
    internationalized translations across supported Fusion 360 languages.
    """
    if not list_items or list_items.count == 0:
        return -1

    # Pass 1: Exact match on name or id
    for i in range(list_items.count):
        item = list_items.item(i)
        name = (getattr(item, 'name', '') or '').strip().lower()
        item_id = (getattr(item, 'id', '') or '').strip().lower()

        if name in SKETCH_NAMES or (item_id and item_id in SKETCH_NAMES):
            return i

    # Pass 2: Substring match on name or id (e.g. in case of accelerator keys or prefixes)
    for i in range(list_items.count):
        item = list_items.item(i)
        name = (getattr(item, 'name', '') or '').strip().lower()
        item_id = (getattr(item, 'id', '') or '').strip().lower()

        for target in SKETCH_NAMES:
            if target in name or (item_id and target in item_id):
                return i

    return -1


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        control = ui.commandDefinitions.itemById('VisibilityOverrideCommand')
        if not control:
            raise RuntimeError("CommandDefinition 'VisibilityOverrideCommand' not found.")

        subcmd = control.controlDefinition
        if not subcmd or not hasattr(subcmd, 'listItems'):
            raise RuntimeError("ControlDefinition or listItems for 'VisibilityOverrideCommand' not found.")

        # Dynamically locate the Sketches item offset across languages
        sketch_index = get_sketch_item_index(subcmd.listItems)

        if sketch_index < 0:
            available_items = []
            for i in range(subcmd.listItems.count):
                item = subcmd.listItems.item(i)
                available_items.append(f"[{i}] name='{getattr(item, 'name', '')}', id='{getattr(item, 'id', '')}'")
            app.log(f"{CMD_NAME}: 'Sketches' not found. Available items: {', '.join(available_items)}", adsk.core.LogLevels.ErrorLogLevel)
            raise RuntimeError(f"Could not locate 'Sketches' option in VisibilityOverrideCommand. Available items: {', '.join(available_items)}")

        # Use the located offset to get the item and toggle its visibility state
        sub = subcmd.listItems.item(sketch_index)
        sub.isSelected = not sub.isSelected
        app.log(f'{CMD_NAME} Sketch visibility located at offset {sketch_index} ({getattr(sub, "name", "")}) and toggled. Now {str(sub.isSelected)}')

    except Exception as e:
        futil.handle_error('command_created')
        if ui:
            ui.messageBox(f'Sketch visibility Update Failed: {str(e)}\nContact the add-in provider\n')
