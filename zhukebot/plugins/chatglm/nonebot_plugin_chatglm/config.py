from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseSettings
from torch import compile, cuda
from transformers import AutoModel, AutoTokenizer, AutoModelForSeq2SeqLM


class Config(BaseSettings):
    chatglm_model: str = "THUDM/chatglm-6b-int4-qe"
    """ChatGLM 模型路径，可用HuggingFace Hub格式（将远程加载），默认使用INT-QE模型，降低硬件需求及压力"""
    chatglm_mode: str = "cpu"
    """模型加载模式，默认CPU加载"""
    chatglm_cmd: list = ["hi"]
    """调用机器人命令"""
    chatglm_cd: int = 60
    """冷却时间"""
    chatglm_record: str = "./data/chatglm/"
    """历史记录存放路径"""
    chatglm_memo: int = 10
    """记录对话轮数"""
    chatglm_tome: bool = False
    """是否需要at机器人"""
    chatglm_group: bool = False
    """是否群聊共用记录"""
    chatglm_pic: bool = False
    """是否转图片"""
    chatglm_width: int = 640
    """图片宽度"""
    nickname: list[str] = ["ChatGLM"]
    """机器人的昵称"""

    class Config:
        extra = "ignore"


def torch_gc():
    if cuda.is_available():
        with cuda.device(CUDA_DEVICE):
            cuda.empty_cache()
            cuda.ipc_collect()


config = Config(**get_driver().config.dict())  # 格式化加载配置
tokenizer = AutoTokenizer.from_pretrained(
    config.chatglm_model, trust_remote_code=True, revision="main"
)
# model = AutoModelForSeq2SeqLM.from_pretrained("THUDM/chatglm-6b-int4-qe")
if config.chatglm_mode.lower() == "cuda":
    model = (
        AutoModel.from_pretrained(
            config.chatglm_model, trust_remote_code=True, revision="main"
        )
        .half()
        .cuda()
    )
    DEVICE = "cuda"
    DEVICE_ID = "0"
    CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE
else:
    model = AutoModel.from_pretrained(
        config.chatglm_model, trust_remote_code=True, revision="main"
    ).float()

model = compile(model).eval()

cd = {}
nickname = config.nickname[0]
logger.debug(f"启用{config.chatglm_mode}模式")
