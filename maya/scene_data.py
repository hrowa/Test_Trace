import maya.cmds as cmds
import json
import os
import time
import requests


def save_scene_geometry_info_ui():

    if cmds.window("saveSceneInfoUI", exists=True):
        cmds.deleteUI("saveSceneInfoUI")

    scene_name = cmds.file(q=True, sn=True).split('/')[-1].rsplit('.', 1)[0]
    settings_file = os.path.join(cmds.workspace(q=True, rd=True), f"{scene_name}_scene_geometry_settings.json")
    settings = load_settings(settings_file)

    window = cmds.window("saveSceneInfoUI", title="Сохранение информации о сцене", widthHeight=(400, 500))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label="Путь для сохранения JSON:")
    default_path = os.path.join(cmds.workspace(q=True, rd=True), f"{scene_name}_scene_geometry_info.json")
    output_file_field = cmds.textField(text=default_path)


    def choose_file():
        file_path = cmds.fileDialog2(fileMode=0, caption="Выберите файл для сохранения", fileFilter="*.json")
        if file_path:
            cmds.textField(output_file_field, e=True, text=file_path[0])

    cmds.button(label="Выбрать JSON-файл...", command=lambda _: choose_file())

    cmds.text(label="Параметры сцены:")
    global_params = {
        "scene_name": cmds.checkBox(label="Название сцены", value=settings["global"].get("scene_name", True)),
        "scene_size_kb": cmds.checkBox(label="Размер файла сцены", value=settings["global"].get("scene_size_kb", True)),
        "timestamp": cmds.checkBox(label="Время обработки", value=settings["global"].get("timestamp", True)),
        "image": cmds.checkBox(label="Сохранить скриншот сцены", value=settings["global"].get("image", True)),
    }

    cmds.text(label="Параметры геометрии:")
    geometry_params = {
        "name": cmds.checkBox(label="Имя объекта", value=settings["geometry"].get("name", True)),
        "is_visible": cmds.checkBox(label="Состояние видимости", value=settings["geometry"].get("is_visible", True)),
        "vertex_count": cmds.checkBox(label="Количество точек", value=settings["geometry"].get("vertex_count", True)),
        "uv_channel_count": cmds.checkBox(label="Количество UV-каналов",
                                          value=settings["geometry"].get("uv_channel_count", True)),
        "child_count": cmds.checkBox(label="Количество дочерних объектов",
                                     value=settings["geometry"].get("child_count", True)),
        "layer_name": cmds.checkBox(label="Название группы/слоя", value=settings["geometry"].get("layer_name", True)),
    }


    def on_save_clicked(*args):
        output_file = cmds.textField(output_file_field, q=True, text=True)
        if not output_file.endswith(".json"):
            cmds.warning("Укажите путь с расширением .json!")
            return

        selected_params = {
            "global": {key: cmds.checkBox(value, q=True, value=True) for key, value in global_params.items()},
            "geometry": {key: cmds.checkBox(value, q=True, value=True) for key, value in geometry_params.items()},
        }

        settings["output_file"] = output_file
        settings["global"] = selected_params["global"]
        settings["geometry"] = selected_params["geometry"]
        save_settings(settings_file, settings)

        save_scene_geometry_info(output_file, selected_params)
        cmds.confirmDialog(title="Готово", message=f"Данные сохранены в {output_file}")

    cmds.button(label="Сохранить", command=on_save_clicked)


    def send_to_server_clicked(*args):
        output_file = cmds.textField(output_file_field, q=True, text=True)

### Saving before sending to server

        selected_params = {
            "global": {key: cmds.checkBox(value, q=True, value=True) for key, value in global_params.items()},
            "geometry": {key: cmds.checkBox(value, q=True, value=True) for key, value in geometry_params.items()},
        }
        save_scene_geometry_info(output_file, selected_params)

        try:
            with open(output_file, 'r') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                cmds.confirmDialog(title="Ошибка", message="JSON должен содержать объект, а не список.")
                return

            url = "http://127.0.0.1:8000/api/save-data/"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=data, headers=headers)

            if response.status_code in (200, 201):
                cmds.confirmDialog(title="Успех", message="Данные успешно отправлены на сервер!")
            else:
                cmds.confirmDialog(title="Ошибка", message=f"Ошибка отправки: {response.status_code}\n{response.text}")

        except Exception as e:
            cmds.confirmDialog(title="Ошибка", message=f"Ошибка при отправке: {str(e)}")

    cmds.button(label="Отправить на сервер", command=send_to_server_clicked)

    cmds.showWindow(window)

### run in headless mode

def save_scene_geometry_info_headless():
    scene_name = cmds.file(q=True, sn=True).split('/')[-1].rsplit('.', 1)[0]

    settings_file = os.path.join(cmds.workspace(q=True, rd=True), f"{scene_name}_scene_geometry_settings.json")
    settings = load_settings(settings_file)

    output_file = settings.get("output_file", os.path.join(cmds.workspace(q=True, rd=True), f"{scene_name}_scene_geometry_info.json"))
    save_scene_geometry_info(output_file, settings)

    try:
        with open(output_file, 'r') as f:
            data = json.load(f)

        if not isinstance(data, dict):
            print("Ошибка: JSON должен содержать объект, а не список.")
            return

        url = "http://127.0.0.1:8000/api/save-data/"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        if response.status_code in (200, 201):
            print("Данные успешно отправлены на сервер!")
        else:
            print(f"Ошибка отправки: {response.status_code}\n{response.text}")

    except Exception as e:
        print(f"Ошибка при отправке: {str(e)}")

### checkbox history

def save_settings(settings_file, settings):
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"Ошибка при сохранении настроек: {e}")


def load_settings(settings_file):
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except (IOError, ValueError):
            pass
    return {
        "output_file": "",
        "global": {},
        "geometry": {}
    }


def save_scene_geometry_info(output_path, selected_params):
    start_time = time.time()

    scene_info = {}
    if selected_params["global"].get("scene_name", False):
        scene_info["scene_name"] = cmds.file(q=True, sn=True).split('/')[-1]
    if selected_params["global"].get("scene_size_kb", False):
        scene_file = cmds.file(q=True, sn=True)
        scene_info["scene_size_kb"] = os.path.getsize(scene_file) if os.path.isfile(scene_file) else 0
    if selected_params["global"].get("timestamp", False):
        scene_info["timestamp"] = time.time() - start_time
    if selected_params["global"].get("image", False):
        screenshot_path = os.path.splitext(output_path)[0] + "_screenshot.png"
        scene_info["image"] = save_scene_screenshot(screenshot_path)

### collecting geo data

    geometry_data = {}
    all_poly_objects = cmds.ls(type="mesh", long=True)

    for poly_obj in all_poly_objects:
        transform = cmds.listRelatives(poly_obj, parent=True, fullPath=True)[0]
        obj_name = transform.split('|')[-1]
        obj_data = {}

        if selected_params["geometry"].get("name", False):
            obj_data["name"] = transform
        if selected_params["geometry"].get("is_visible", False):
            obj_data["is_visible"] = cmds.getAttr(f"{transform}.visibility")
        if selected_params["geometry"].get("vertex_count", False):
            obj_data["vertex_count"] = cmds.polyEvaluate(poly_obj, vertex=True)
        if selected_params["geometry"].get("uv_channel_count", False):
            uv_sets = cmds.polyUVSet(poly_obj, query=True, allUVSets=True) or []
            obj_data["uv_channel_count"] = len(uv_sets)
        if selected_params["geometry"].get("child_count", False):
            children = cmds.listRelatives(transform, children=True) or []
            obj_data["child_count"] = len(children)
        if selected_params["geometry"].get("layer_name", False):
            group_or_layer = None
            parent = cmds.listRelatives(transform, parent=True, fullPath=True)
            if parent:
                group_or_layer = parent[0]
            display_layers = cmds.listConnections(transform, type="displayLayer")
            if display_layers:
                group_or_layer = display_layers[0]
            obj_data["layer_name"] = group_or_layer

        if obj_data:
            geometry_data[obj_name] = obj_data

    scene_info["geometry"] = geometry_data

### creating json

    try:
        with open(output_path, 'w') as f:
            json.dump(scene_info, f, indent=4)
        print(f"Информация успешно сохранена в {output_path}")
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")

### saving screenshot

def save_scene_screenshot(output_path):
    all_objects = cmds.ls(transforms=True, long=True)
    hidden_objects = [obj for obj in all_objects if not cmds.getAttr(f"{obj}.visibility")]
    for obj in hidden_objects:
        cmds.setAttr(f"{obj}.visibility", True)
    cmds.select(clear=True)
    cmds.viewFit()
    cmds.playblast(completeFilename=output_path, forceOverwrite=True, format="image", viewer=False, showOrnaments=False)
    for obj in hidden_objects:
        cmds.setAttr(f"{obj}.visibility", False)

    return output_path


save_scene_geometry_info_ui()
