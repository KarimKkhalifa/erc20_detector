import re

ALLOWED_TOKENS = [
    "IERC20", "IERC20Metadata", "ERC20", "IERC20Permit", "ERC20Permit",
    "ERC20Burnable", "ERC20Capped", "ERC20Pausable", "ERC20Votes",
    "ERC20Wrapper", "ERC20FlashMint", "ERC1363", "ERC4626", "SafeERC20"
]

# Create the regex pattern for allowed tokens
allowed_tokens_regex = '|'.join([re.escape(token) for token in ALLOWED_TOKENS])
REGEX_PATTERN = re.compile(
    rf'\bimport\s+["\']@openzeppelin/contracts(?:/[\w\d]+)*/({allowed_tokens_regex})(?:\.sol)?["\'];'
)
