from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


def de_eblanify(string: str) -> str:
    if string == '__root__':
        return string
    # if string == 'friendof_count':
    #     return 'friendOfCount'
    result: str = ''.join(word.capitalize() for word in string.split('_'))
    if len(result) > 0:
        result = result[0].lower() + result[1:]
    return result


class Verdict(str, Enum):
    FAILED = "FAILED"
    OK = "OK"
    PT = "PARTIAL"
    CE = "COMPILATION_ERROR"
    RE = "RUNTIME_ERROR"
    WA = "WRONG_ANSWER"
    PE = "PRESENTATION_ERROR"
    TL = "TIME_LIMIT_EXCEEDED"
    ML = "MEMORY_LIMIT_EXCEEDED"
    IL = "IDLENESS_LIMIT_EXCEEDED"
    SV = "SECURITY_VIOLATED"
    CRASHED = "CRASHED"
    INPUT_PREPARATION_CRASHED = "INPUT_PREPARATION_CRASHED"
    CHALLENGED = "CHALLENGED"
    SK = "SKIPPED"
    TESTING = "TESTING"
    RJ = "REJECTED"


class HackVerdict(str, Enum):
    HACK_SUCCESSFUL = "HACK_SUCCESSFUL"
    HACK_UNSUCCESSFUL = "HACK_UNSUCCESSFUL"
    INVALID_INPUT = "INVALID_INPUT"
    GENERATOR_INCOMPILABLE = "GENERATOR_INCOMPILABLE"
    GENERATOR_CRASHED = "GENERATOR_CRASHED"
    IGNORED = "IGNORED"
    TESTING = "TESTING"
    OTHER = "OTHER"


class ContestType(str, Enum):
    CF = "CF"
    IOI = "IOI"
    ICPC = "ICPC"


class ContestPhase(str, Enum):
    BEFORE = "BEFORE"
    CODING = "CODING"
    PENDING_SYSTEM_TEST = "PENDING_SYSTEM_TEST"
    SYSTEM_TEST = "SYSTEM_TEST"
    FINISHED = "FINISHED"


class ProblemResultType(str, Enum):
    PRELIMINARY = "PRELIMINARY"
    FINAL = "FINAL"


class APIModel(BaseModel):
    class Config:
        alias_generator = de_eblanify


class JudgeProtocol(APIModel):
    manual: bool
    protocol: Optional[str] = None
    verdict: Optional[str] = None


class BlogEntry(APIModel):
    id: int
    original_locale: str
    creation_time_seconds: int
    author_handle: str
    title: str
    content: Optional[str] = None
    locale: str
    modification_time_seconds: int
    allow_view_history: bool
    tags: List[str]
    rating: int


class Comment(APIModel):
    id: int
    creation_time_seconds: int
    commentator_handle: str
    locale: str
    text: str
    parent_comment_id: Optional[int] = None
    rating: int


class RecentAction(APIModel):
    time_seconds: int
    blog_entry: BlogEntry
    comment: Comment


class ProblemStatistics(APIModel):
    contest_id: int
    index: str
    solved_count: int


class RatingChange(APIModel):
    contest_id: int
    contest_name: str
    handle: str
    rank: int
    rating_update_time_seconds: int
    old_rating: int
    new_rating: int


class Member(APIModel):
    handle: str


class Problem(APIModel):
    contest_id: Optional[int] = None
    problem_set_name: Optional[str] = None
    index: str
    name: str
    type: str
    points: Optional[float] = None
    rating: Optional[int] = None
    tags: List[str]


class User(APIModel):
    handle: str
    email: Optional[str] = None
    vk_id: Optional[str] = None
    open_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    organization: Optional[str] = None
    contribution: int
    rank: str
    rating: int
    max_rank: str
    max_rating: int
    last_online_time_seconds: int
    registration_time_seconds: int
    friendof_count: int
    avatar: str
    title_photo: str


class Party(APIModel):
    contest_id: int
    members: List[Member]
    participant_type: str
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    ghost: bool
    room: Optional[int] = None
    start_time_seconds: Optional[int] = None


class Submission(APIModel):
    id: int
    contest_id: int
    creation_time_seconds: int
    relative_time_seconds: int
    problem: Problem
    author: Party
    programming_language: str
    verdict: Optional[Verdict] = None
    testset: str
    passed_test_count: int
    time_consumed_millis: int
    memory_consumed_bytes: int
    points: Optional[float] = None


class Contest(APIModel):
    id: int
    name: str
    type: ContestType
    phase: ContestPhase
    frozen: bool
    duration_seconds: bool
    start_time_seconds: Optional[int] = None
    relative_time_seconds: Optional[int] = None
    prepared_by: Optional[str] = None
    website_url: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[int] = None
    kind: Optional[str] = None
    icpc_region: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    season: Optional[str] = None


class Hack(APIModel):
    id: int
    creation_time_seconds: int
    hacker: Party
    defender: Party
    problem: Problem
    test: Optional[str] = None
    judge_protocol: JudgeProtocol


class ProblemResult(APIModel):
    points: float
    penalty: int
    rejected_attempt_count: int
    type: ProblemResultType
    best_submission_time_seconds: int


class RanklistRow(APIModel):
    party: Party
    rank: int
    points: float
    penalty: int
    successful_hack_count: int
    unsuccessful_hack_count: int
    problem_result: List[ProblemResult]
    last_submission_time_seconds: int


class Sample(BaseModel):
    s_in: str
    s_out: str
