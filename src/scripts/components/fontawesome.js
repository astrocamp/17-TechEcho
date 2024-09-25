import { library, dom } from "@fortawesome/fontawesome-svg-core";
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
    faThumbsUp,
    faHeart,
} from "@fortawesome/free-solid-svg-icons";

import {
    faCalendar,
} from "@fortawesome/free-regular-svg-icons";

// Add icons to the library
library.add(
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
    faThumbsUp,
    faHeart,
    faSolidHeart,
    faRegularHeart,
);

// Initialize Font Awesome
dom.watch(); // Watches for changes in the DOM and renders icons accordingly

// Initialize Alpine.js
window.Alpine = Alpine;
Alpine.start();
