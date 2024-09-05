import { library, dom } from "@fortawesome/fontawesome-svg-core"

import { faBookmark as fasBookmark, faMagnifyingGlass, faArrowUp, faArrowDown} from "@fortawesome/free-solid-svg-icons"
import { faBookmark as farBookmark } from "@fortawesome/free-regular-svg-icons"


library.add(farBookmark, fasBookmark, faMagnifyingGlass, faArrowUp, faArrowDown)

dom.i2svg()