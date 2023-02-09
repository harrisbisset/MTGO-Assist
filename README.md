## MTGO Assistant Tool
v1.0.0

## License
[MIT License](LICENSE)


78h spent programming

        #format is currently not discerable from the logs, so this should always be true
        if format is not None:
            #finds the format <select> tag, and selects the format passed in
            selectElement = self.driver.find_element(By.XPATH, '//body/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[4]/td[2]/select')
            selectObject = Select(selectElement)
            selectObject.select_by_visible_text(format)
