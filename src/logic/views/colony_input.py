from game.commands import CloseInfoPanelCommand, OpenInteractableMenuCommand
from game.interactions import ActionProxy


def handle_colony_input(view, cmd: dict) -> None:
    """Handle raw input for ColonyView."""
    cmd_type = cmd.get("type")

    if cmd_type == "mouse_press":
        _handle_mouse_press(view, cmd)
    elif cmd_type == "mouse_move":
        view._handle_camera_drag(cmd.get("pos"))
    elif cmd_type == "mouse_release":
        view._stop_camera_drag()
    elif cmd_type == "key_press":
        _handle_key_press(view, cmd)
    elif cmd_type == "wheel":
        view._handle_wheel_zoom(cmd.get("delta"))
    else:
        print(f"Unknown input type: {cmd_type}")


def _handle_mouse_press(view, cmd: dict) -> None:
    """Route mouse press input by button."""
    pos = cmd.get("pos")
    button = cmd.get("button")
    if pos is None:
        return

    if button == "left":
        _handle_left_click(view, pos)
    elif button == "right":
        _handle_right_click(view, pos)
    elif button == "middle":
        view._start_camera_drag(pos)


def _handle_left_click(view, pos: tuple[int, int]) -> None:
    """Handle selection and overlay clicks."""
    if _handle_interaction_panel_click(view, pos):
        return

    if _handle_info_panel_click(view, pos):
        return

    grid = view._screen_to_grid(pos)
    view.selected_entity_id = view._select_entity_at_grid(grid)


def _handle_right_click(view, pos: tuple[int, int]) -> None:
    """Handle interactable target or selected entity movement."""
    if view._command_queue is None:
        return

    grid = view._screen_to_grid(pos)
    interactable_entity_id = view._get_interactable_entity_at_grid(grid)
    if interactable_entity_id is not None:
        view._interaction_target_entity_id = interactable_entity_id
        view._command_queue.push(
            OpenInteractableMenuCommand(
                view.world_id,
                interactable_entity_id,
            )
        )
        return

    if view.selected_entity_id is None:
        return
    view._interaction_target_entity_id = None

    view._push_move_command(view.selected_entity_id, grid)


def _handle_key_press(view, cmd: dict) -> None:
    """Handle keyboard input."""


def _handle_info_panel_click(view, pos: tuple[int, int]) -> bool:
    """Close info panel when clicking its close rect."""
    panel = view._get_current_info_panel()
    if panel is None:
        return False

    close_rect = panel.get("close_rect")
    if close_rect is None:
        return False

    if not _point_in_rect(pos, close_rect):
        return False

    if view._command_queue is not None:
        view._command_queue.push(
            CloseInfoPanelCommand(
                view.world_id,
                panel.get("panel_id", "panel"),
            )
        )

    return True


def _handle_interaction_panel_click(view, pos: tuple[int, int]) -> bool:
    """Handle action clicks on the interaction menu."""
    panel = view._get_current_info_panel()
    if panel is None or panel.get("panel_id") != "interaction_menu":
        return False

    for action in panel.get("actions", []):
        action_rect = action.get("rect")
        if action_rect is None:
            continue
        if not _point_in_rect(pos, action_rect):
            continue
        action_id = action.get("action_id")
        if action_id == "move_to":
            _push_move_to_interaction(view)
        else:
            _push_action_interaction(view, str(action_id))
        return True

    return False


def _push_action_interaction(view, action_id: str) -> None:
    """Push command created by ActionProxy for active target."""
    if (
        view._command_queue is None
        or view._interaction_target_entity_id is None
    ):
        return

    command = ActionProxy.create_command(
        action_id=action_id,
        data={
            "world_id": view.world_id,
            "actor_entity_id": view.selected_entity_id,
            "target_entity_id": view._interaction_target_entity_id,
            "entity_id": view._interaction_target_entity_id,
        },
    )
    if command is not None:
        view._command_queue.push(command)


def _push_move_to_interaction(view) -> None:
    """Move selected entity to the active interaction target."""
    if (
        view.selected_entity_id is None
        or view._interaction_target_entity_id is None
    ):
        return

    grid = view._get_entity_grid(view._interaction_target_entity_id)
    if grid is None:
        return

    view._push_move_command(view.selected_entity_id, grid)
    _close_interaction_menu(view)


def _close_interaction_menu(view) -> None:
    """Close active interaction menu panel."""
    if view._command_queue is None:
        return

    view._command_queue.push(
        CloseInfoPanelCommand(
            view.world_id,
            "interaction_menu",
        )
    )


def _point_in_rect(pos: tuple[int, int], rect: list) -> bool:
    """Return whether screen pos is inside rect."""
    x, y = pos
    rect_x, rect_y, width, height = [int(value) for value in rect]
    return rect_x <= x <= rect_x + width and rect_y <= y <= rect_y + height
