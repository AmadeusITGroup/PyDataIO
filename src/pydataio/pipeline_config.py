from .job_config import JobConfig
from .transformer import Transformer


class PipelineConfig:
    """
    Class to represent a pipeline configuration
    """

    transformer: Transformer
    JobConfig: JobConfig

    def __init__(self, transformer: Transformer, JobConfig: JobConfig):
        self.transformer = transformer
        self.JobConfig = JobConfig
