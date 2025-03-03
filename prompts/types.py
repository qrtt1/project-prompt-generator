from dataclasses import dataclass


@dataclass(frozen=True)
class FileEntry:
    sequence: int
    relative_path: str
    filename: str
    file_full_path: str

    @property
    def md_filename(self):
        return f"{str(self.sequence).zfill(3)}_{self.relative_path}"
