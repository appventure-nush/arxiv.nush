/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import { loadFonts } from "./webfontloader";
import vuetify from "./vuetify";
import pinia from "../store";
import router from "../router";

// Types
import type { App } from "vue";

// import mavonEditor from 'mavon-editor'
// import 'mavon-editor/dist/css/index.css'

// import FileSelector main css
import "vue-file-selector/dist/main.css";
// import the FileSelector plugin
import FileSelector from "vue-file-selector";

export function registerPlugins(app: App) {
  loadFonts();
  app.use(vuetify).use(router).use(pinia).use(FileSelector);
}
