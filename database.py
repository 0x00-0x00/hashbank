from shemutils.database import *

t1 = Table("HashBank",
    {
        "PLAIN_TEXT": TEXT,
        "HASH": TEXT,
    }
)
