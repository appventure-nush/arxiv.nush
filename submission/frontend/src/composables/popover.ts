import { ref, type Ref } from "vue";
import { createPopper } from "@popperjs/core";

export function usePopover(popoverRef: Ref<HTMLElement | null>) {
  // state encapsulated and managed by the composable
  const popoverShow: Ref<any> = ref(false);
  const todaysEvent: Ref<any> = ref({});

  /**
   * Open or closes the popover
   * @param {event} evt The click event handler
   * @returns
   */
  const togglePopover = (evt: any, todaysEvt: any) => {
    if (popoverShow.value == false) {
      todaysEvent.value = todaysEvt;
      popoverShow.value = true;
      createPopper(evt.target, popoverRef.value ?? new HTMLElement(), {
        placement: "bottom",
      });
      return;
    }

    popoverShow.value = false;
    todaysEvent.value = {};
  };

  // expose managed state as return value
  return { popoverShow, todaysEvent, togglePopover };
}
