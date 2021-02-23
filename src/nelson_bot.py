import logging
import time

from selenium import webdriver
from src.brown_authentication import BrownAuthentication
from src.bot import Bot

logger = logging.getLogger()


class NelsonBot:

    def __init__(self):
        self.bot = Bot()

    @staticmethod
    def __search_slots(driver: webdriver, spot_preferences: list) -> list:
        """Searches the booking page for the the preferred timeslots on a given day"""
        # disable buffer to scan page
        driver.implicitly_wait(0)

        # check for slots that match slot preferences and store onClick() reference
        slots = []
        for slot in spot_preferences:
            found_slot = driver.find_elements_by_xpath(f"//p[./strong[starts-with(text(), '{slot}')]]")
            if len(found_slot) > 0:
                logger.info(f"Found the {slot} time slot")
                wrapper = found_slot[0].find_element_by_xpath("./..")
                book_now_button = wrapper.find_elements_by_xpath('//button[text()="Book Now"]')

                # check if book now button was found
                if len(book_now_button) > 0:
                    slots.append(book_now_button[0].get_attribute("onclick"))
                else:
                    logger.error("This user already has a reservation for this day!")
                    raise Exception("Slot is already booked for this day!")

        driver.implicitly_wait(2)

        return slots

    @staticmethod
    def __book_slots(driver: webdriver, slots: list) -> bool:
        for slot in slots:
            # Attempt to book slot
            logger.info(f"Attempting to reserve time slot...")
            driver.execute_script(slot)
            time.sleep(1)
            success_alert = driver.find_element_by_id("alertBookingSuccess")

            if success_alert.get_attribute("style") == "display: block;":
                # Booking successful
                logger.info(f"Booked time slot!")
                return True
            else:
                logger.info(f"Failed to book time slot...")
                driver.refresh()

        logger.info(f"None of the preferred time slots were available")
        return False

    def start(self, month: int, day: int, year: int, username: str, password: str, duo_bypass: str,
              slot_preferences: list, refresh_count: int, refresh_interval: int) -> bool:
        chrome_options = self.bot.get_default_chrome_options()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(4)

        # Open reservation portal
        driver.get("https://bfit.brownrec.com/booking/4a42ba76-754b-48c9-95fd-8df6d4e3fb4d")
        time.sleep(1)

        # Authenticate with credentials
        driver.execute_script("submitExternalLoginForm('Shibboleth')")
        time.sleep(3)
        BrownAuthentication.authenticate(driver, username, password, duo_bypass)

        # Fetch available time slots
        logger.info(f"Searching for available time slots on {month}/{day}/{year}...")
        driver.execute_script(
            f"window.open('https://bfit.brownrec.com/booking/4a42ba76-754b-48c9-95fd-8df6d4e3fb4d/slots/c1ae8801-310e-42ef-ba3b-3bd93e06cc00/{year}/{month}/{day}', '_blank')")
        driver.switch_to.window(driver.window_handles[1])

        # Check if desired time slots are available
        slots = self.__search_slots(driver, slot_preferences)
        booking_successful = False

        for attempt in range(refresh_count):
            if len(slots) > 0:
                # Slots found
                driver.switch_to.window(driver.window_handles[0])
                booking_successful = self.__book_slots(driver, slots)
                break
            else:
                # Slots not yet available... retry
                logger.info(f"Slots not yet available! Retry {attempt + 1}/{refresh_count}")
                time.sleep(refresh_interval)
                driver.refresh()
                slots = self.__search_slots(driver, slot_preferences)

        if booking_successful:
            logger.info("Booking successful!")
        else:
            logger.info("Booking failed!")

        driver.quit()

        return booking_successful

    def close(self):
        # Remove specific tmp dir of this "run"
        self.bot.close()
