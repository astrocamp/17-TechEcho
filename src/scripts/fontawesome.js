import { library, dom } from "@fortawesome/fontawesome-svg-core"
import { faBookmark as fasBookmark, faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark } from "@fortawesome/free-regular-svg-icons"


library.add(farBookmark, fasBookmark, faMagnifyingGlass)
dom.i2svg()