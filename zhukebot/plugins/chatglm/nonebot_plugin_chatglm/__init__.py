from nonebot.plugin import PluginMetadata

from . import config, chat, help

# from .chatpdf import *


__plugin_meta__ = PluginMetadata(
    name="ChatGLM聊天",
    description="基于chatGLM-6B模型提供机器人对话聊天",
    usage="hi[聊天内容]，清空记录，导出记录",
    extra={
        "author": "daomingze",
        "version": "0.1.5",
        "priority": 8,
    },
)
