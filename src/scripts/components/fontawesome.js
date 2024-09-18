import { library, dom } from "@fortawesome/fontawesome-svg-core"



import { faMagnifyingGlass, faArrowUp, faArrowDown, faBell,faUser,faCalendarCheck,faClockRotateLeft,faPen,faCalendar} from "@fortawesome/free-solid-svg-icons"

import Alpine from 'alpinejs';

library.add(faBell, faMagnifyingGlass, faArrowUp, faArrowDown,faUser,faCalendarCheck,faClockRotateLeft,faPen,faCalendar)


dom.i2svg()

Alpine.data("convert_to_svg", () => ({
    init() {
        dom.i2svg();
    },
}))

