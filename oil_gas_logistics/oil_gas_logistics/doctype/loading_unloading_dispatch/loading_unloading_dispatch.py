# Copyright (c) 2023, botan.b.abdullah@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LoadingUnloadingDispatch(Document):

    IN_TRANSACTION_TYPE = 'IN'
    
    def validate(self):
        # Call functions based on the changes in the form
        self.calculate_difference_in_weight()
        self.calculate_net_weight_in_tonne()
        self.calculate_destination_weight_in_tonne()
        #self.calculate_destination_weight_in_meters()
        self.calculate_weight_in_meters()
        self.calculate_normal_weight_in_meters()
        self.calculate_average_density()
        self.toggle_kirkuk_detail_section()

    def calculate_average_density(self):
        density = float(self.density) if self.density else 0
        suli_standard_density = float(self.suli_standard_density) if self.suli_standard_density else 0
        if density and suli_standard_density:
            self.average_density = (density + suli_standard_density) / 2
        else:
            self.average_density = 0

    def calculate_difference_in_weight(self):
        product_net_weight = float(self.product_net_weight) if self.product_net_weight else 0
        kirkuk_net_weight = float(self.kirkuk_net_weight) if self.kirkuk_net_weight else 0
        self.difference_in_weight = product_net_weight - kirkuk_net_weight

    def calculate_net_weight_in_tonne(self):
        product_net_weight = float(self.product_net_weight) if self.product_net_weight else 0
        self.net_weight_in_tonne = product_net_weight / 1000

    def calculate_destination_weight_in_tonne(self):
        kirkuk_net_weight = float(self.kirkuk_net_weight) if self.kirkuk_net_weight else 0
        self.destination_weight_in_tonne = kirkuk_net_weight / 1000

    # def calculate_destination_weight_in_meters(self):
    #     kirkuk_net_weight = float(self.kirkuk_net_weight) if self.kirkuk_net_weight else 0
    #     kirkuk_standard_density = float(self.kirkuk_standard_density) if self.kirkuk_standard_density else 0
    #     self.destination_weight_in_meters = (kirkuk_net_weight / 1000) / kirkuk_standard_density if kirkuk_standard_density != 0 else 0

    def calculate_weight_in_meters(self):
        product_net_weight = float(self.product_net_weight) if self.product_net_weight else 0
        suli_standard_density = float(self.suli_standard_density) if self.suli_standard_density else 0
        self.weight_in_meters = (product_net_weight / 1000) / suli_standard_density if suli_standard_density != 0 else 0

    def calculate_normal_weight_in_meters(self):
        product_net_weight = float(self.product_net_weight) if self.product_net_weight else 0
        density = float(self.density) if self.density else 0
        self.normal_weight_in_meters = (product_net_weight / 1000) / density if density != 0 else 0

    def autoname(self):
        current_year = datetime.now().strftime('%Y')
        if self.transaction_type == 'IN':
            self.name = f"IN-{self.wb_id}-{current_year}-{self.loading_location}"
        elif self.transaction_type == 'OUT':
            self.name = f"OUT-{self.wb_id}-{current_year}-{self.unloading_location}"
        elif self.transaction_type == 'TRANSFER':
            self.name = f"Transfer-{self.wb_id}-{current_year}-{self.loading_location}-{self.unloading_location}"
        else:
            frappe.throw('Invalid transaction type selected.')

    @frappe.whitelist()
    def get_attached_images(self):
        return frappe.get_all("File", filters={"attached_to_name": self.name, "attached_to_doctype": "Loading Unloading Dispatch", "is_private": 0})

    def toggle_kirkuk_detail_section(self):
        if self.transaction_type == self.IN_TRANSACTION_TYPE:
            # Toggle fields as required
            # Use Frappe's methods/API to set field properties, if needed
            pass
        else:
            # Toggle fields for the else case
            # Again, use Frappe's methods/API if needed
            pass

    # You can add other methods as needed

