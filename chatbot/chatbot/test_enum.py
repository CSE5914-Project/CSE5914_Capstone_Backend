from enum import Enum
class movieSource(Enum):
  default = "popular"
  byId =  "byId"
  byGenere = "byGenere"

x = movieSource.default
print(movieSource.default)
print(movieSource.default.name)
print(movieSource.default.value)
print(type(x.name))