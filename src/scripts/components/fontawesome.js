import { library, dom } from "@fortawesome/fontawesome-svg-core"
import Alpine from 'alpinejs';

import {
    faMagnifyingGlass,
    faGraduationCap,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses,
    faUser,
    faCalendarCheck,
    faClockRotateLeft,
    faPen,
    faCamera,
    faBars,
    faTimes,
    faThumbsUp as fasThumbsUp,
    faThumbsDown as fasThumbsDown
} from "@fortawesome/free-solid-svg-icons"

import {
    faCalendar,
    faThumbsUp as farThumbsUp,
    faThumbsDown as farThumbsDown
} from "@fortawesome/free-regular-svg-icons"

library.add(
    fasThumbsUp,
    fasThumbsDown,
    farThumbsUp,
    farThumbsDown,
    faMagnifyingGlass,
    faGraduationCap,
    faArrowUp,
    faArrowDown,
    faBell,
    faGlasses,
    faUser,
    faCalendarCheck,
    faCalendar,
    faClockRotateLeft,
    faPen,
    faCamera,
    faBars,
    faTimes,
)

dom.i2svg()

Alpine.data("convert_to_svg", () => ({
    init() {
        dom.i2svg();
    },
}))

