# CreatedBy: Emilia Crow
# CreateDate: 20210330
# Updated: 20220209
# CreateFor: Franklin Young International

from Tools.ProgressBar import TextBoxObject
from Tools.ProgressBar import ProgressBarWindow


class IngestionObject:
    def __init__(self, obDal):
        self.name = 'Ingester Nester'
        self.obDal = obDal
        self.load_limit = 50
        self.base_price_collector = []
        self.product_collector = []
        self.product_price_collector = []
        self.product_image_match_collector = []

        self.product_document_collector = []
        self.product_image_collector = []
        self.product_video_collector = []

        self.product_update_asset_collector = []

        self.product_bc_toggle_collector = []
        self.product_discon_collector = []
        self.product_is_visible_collector = []
        self.product_update_image_collector = []
        self.product_notes_collector = []

        self.product_ecat_toggle_collector = []
        self.product_htme_toggle_collector = []
        self.product_gsa_toggle_collector = []
        self.product_va_toggle_collector = []


    def set_progress_bar(self, name, count_of_steps):
        self.obProgressBarWindow = ProgressBarWindow(name)
        self.obProgressBarWindow.show()
        self.obProgressBarWindow.set_anew(count_of_steps)


    def ingest_attribute(self,attribute_desc,table_name):
        return_id = self.obDal.attribute_cap(attribute_desc,table_name)
        return return_id

    # cetegory functions
    def ingest_categories(self, df_categories):
        ingested_set = []
        self.set_progress_bar('Ingesting Categories',len(df_categories.index))
        p_bar = 0

        for column, row in df_categories.iterrows():
            category_string = str(row['Category'])
            category_name = category_string.rpartition('/')[2]

            return_id = self.obDal.category_cap(category_name, category_string)

            ingested_set.append([return_id,category_string])

            p_bar+=1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def ingest_product_category(self, product_id, category_id):
        # this takes a parent child and get the id of the category
        product_category_id = self.obDal.product_category_cap(product_id,category_id)
        return product_category_id

    def get_category_names(self):
        df_category_lookup = self.obDal.get_category_names()
        return df_category_lookup

    def manual_ingest_category(self, name = '', hierarchy = ''):
        lst_req_fields = [['CategoryName', 128, 'This is most likely the bottom level value<br>like "Lab Supplies"',name,'required'],
                          ['CategoryHierarchy', 128, 'This is the full hierarchy<br>like "All Products/Life Science/Lab Supplies"',hierarchy,'required']]
        obTextBox = TextBoxObject(lst_req_fields, title='Create new category')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('CategoryName' in entered_values.keys()) and ('CategoryHierarchy' in entered_values.keys()):
            cat_name = entered_values['CategoryName']
            cat_hierarchy = entered_values['CategoryHierarchy']
        else:
            return 0

        if (cat_name != '') and (cat_hierarchy != '') and ('All Products/' in cat_hierarchy):
            cat_id = self.obDal.category_cap(cat_name, cat_hierarchy)
            new_cat_name = cat_hierarchy.rpartition('/')[2]
            if new_cat_name != cat_name:
                cat_id = self.obDal.category_cap(new_cat_name, cat_hierarchy)

            while ('/' in cat_hierarchy):
                cat_hierarchy = cat_hierarchy.rpartition('/')[0]
                cat_name = cat_hierarchy.rpartition('/')[2]
                level_cat_id = self.obDal.category_cap(cat_name, cat_hierarchy)

            return cat_id
        else:
            return -1

    # country of origin functions
    def ingest_country(self,country,country_long_name,country_code,ecatcode,is_taa_compliant):
        # this should do more than just pass through
        return_id = self.obDal.country_cap(country,country_long_name,country_code,ecatcode,is_taa_compliant)
        return return_id

    def ingest_countries(self,df_countries):
        ingested_set = []
        self.set_progress_bar('Ingesting Countries',len(df_countries.index))
        p_bar = 0

        for column, row in df_countries.iterrows():
            country = str(row['CountryName'])
            country_long_name = str(row['CountryLongName'])
            country_code = str(row['CountryCode'])
            ecatcode = str(row['ECATCountryCode'])
            is_taa_compliant = str(row['IsTAACompliant'])
            return_id = self.ingest_country(country,country_long_name,country_code,ecatcode,is_taa_compliant)
            ingested_set.append([return_id,country,country_long_name,country_code,ecatcode,is_taa_compliant])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def get_country_lookup(self):
        df_country_lookup = self.obDal.get_country_lookup()
        return df_country_lookup

    def manual_ingest_country(self,atmp_name = '',atmp_long_name = '', atmp_code = '', atmp_ecat_code = ''):
        is_taa_compliant = '0'
        lst_req_fields = [['CountryName', 45, 'This is a common name<br>like "The Congo"',atmp_name,'required'],
                          ['LongCountryName', 128, 'This is a full name<br>like "Democratic Republic of the Congo"',atmp_long_name,'required'],
                          ['CountryCode', 2, 'This is the 2 letter code, "CG"',atmp_code,'required'],
                          ['CountryCodeEcat', 3, 'This is the 3 letter code, "178"',atmp_ecat_code,'required'],
                          ['IsTAACompliant', 1, 'This is 1 or 0',is_taa_compliant,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title= 'Country of origin entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('CountryName' in entered_values.keys()) and ('LongCountryName' in entered_values.keys()) and ('CountryCode' in entered_values.keys()) and ('CountryCodeEcat' in entered_values.keys()):
            country_name = entered_values['CountryName'].upper()
            full_country_name = entered_values['LongCountryName']
            country_code = entered_values['CountryCode'].upper()
            country_code_ecat = entered_values['CountryCodeEcat'].upper()
            is_taa_compliant = int(entered_values['IsTAACompliant'])
        else:
            return 0

        if (country_name != '') and (full_country_name != '') and (country_code != '') and (country_code_ecat != ''):
            coo_id = self.obDal.country_cap(country_name, full_country_name, country_code, country_code_ecat, is_taa_compliant)
            return coo_id
        else:
            return -1

    # fsc code functions
    def ingest_fsc(self,fsc_code,fsc_name,fsc_desc=''):
        return_id = self.obDal.fsc_code_cap(fsc_code,fsc_name,fsc_desc)
        return return_id

    def ingest_fscs(self,df_fscs):
        ingested_set = []
        self.set_progress_bar('Ingesting FSCs',len(df_fscs.index))
        p_bar = 0
        for column, row in df_fscs.iterrows():
            fsc_code = str(row['FSCCode'])
            fsc_name = str(row['FSCName'])
            fsc_desc = str(row['FSCDesc'])

            return_id = self.ingest_fsc(fsc_code,fsc_name,fsc_desc)
            ingested_set.append([return_id,fsc_code,fsc_name,fsc_desc])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def manual_ingest_fsc_code(self,atmp_code = '', atmp_name = '', atmp_desc = ''):
        lst_req_fields = [['FSCCode',15,'This is a sample code<br>like "AF11"',atmp_code,'required'],
                          ['FSCCodeName',128,'This is the title<br>like "EDUCATION (BASIC)"',atmp_name,'required'],
                          ['FSCCodeDesc',128,'Any additional info<br>like "EDUCATION - BASIC RESEARCH"',atmp_desc,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title='FSC code entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('FSCCode' in entered_values.keys()) and ('FSCCodeName' in entered_values.keys()) and ('FSCCodeDesc' in entered_values.keys()):
            fsc_code = entered_values['FSCCode']
            fsc_code_name = entered_values['FSCCodeName']
            fsc_code_desc = entered_values['FSCCodeDesc']
        else:
            return 0

        if (fsc_code != '') and (fsc_code_name != '') and (fsc_code_desc != ''):
            fsc_id = self.obDal.fsc_code_cap(fsc_code, fsc_code_name, fsc_code_desc)
            return fsc_id
        else:
            return -1

    # hazard code functions
    def ingest_hazard_code(self, hazard_code, hazard_desc, hazard_cat=''):
        return_id = self.obDal.hazardous_code_cap(hazard_code, hazard_desc, hazard_cat)
        return return_id

    def ingest_hazard_codes(self, df_hazard_codes):
        ingested_set = []
        self.set_progress_bar('Ingesting Hazard Codes',len(df_hazard_codes.index))
        p_bar = 0
        for column, row in df_hazard_codes.iterrows():
            hazard_code = str(row['HazardousCode'])
            hazard_desc = str(row['HazDesc'])

            return_id = self.ingest_hazard_code(hazard_code, hazard_desc)
            ingested_set.append([return_id, hazard_code, hazard_desc])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def manual_ingest_hazard_code(self,atmp_code = '', atmp_desc = ''):
        lst_req_fields = [['HazardCode',45,'This is the code<br>like "NA1270"',atmp_code,'required'],
                          ['HazardDesc',256,'This is the description<br>like "Petroleum oil"',atmp_desc,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title='Hazard code entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('HazardCode' in entered_values.keys()) and ('HazardDesc' in entered_values.keys()):
            hazard_code = entered_values['HazardCode']
            hazard_desc = entered_values['HazardDesc']
        else:
            return 0

        if (hazard_code != '') and (hazard_desc != ''):
            haz_id = self.obDal.hazardous_code_cap(hazard_code, hazard_desc)
            return haz_id
        else:
            return -1

    # manufacturer functions
    def ingest_manufacturer(self, manufacturer_name, supplier_name, manufacturer_prefix = -1):
        return_id = self.obDal.manufacturer_cap(manufacturer_name, supplier_name, manufacturer_prefix)
        return return_id

    def ingest_manufacturers(self,df_manufacturers):
        ingested_set = []
        self.set_progress_bar('Ingesting Manufacturers',len(df_manufacturers.index))
        p_bar = 0

        for column, row in df_manufacturers.iterrows():
            manufacturer_prefix = -1
            supplier_name = str(row['SupplierName'])
            supplier_name = supplier_name.strip().lower()
            manufacturer_name = str(row['ManufacturerName'])

            if (row['FYManufacturerPrefix'] != ''):
                manufacturer_prefix = int(row['FYManufacturerPrefix'])

            return_id = self.ingest_manufacturer(manufacturer_name,supplier_name,manufacturer_prefix)
            ingested_set.append([return_id,manufacturer_name,supplier_name,manufacturer_prefix])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def get_manufacturer_lookup(self):
        df_manufacturer_lookup = self.obDal.get_manufacturer_lookup()
        return df_manufacturer_lookup

    def manual_ingest_manufacturer(self, atmp_sup = '', atmp_man = '',lst_manufacturer_names=[]):
        lst_req_fields = [['SupplierName',45,'This is the ugly version of the name<br>like "thermo electron (karlsruhe) gmbh"', atmp_sup,'required'],
                          ['ManufacturerName',45,'This is the standardized name<br>like "THERMO ELECTRON"', atmp_man,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title='Manufacturer entry',lst_for_dropdown=lst_manufacturer_names)
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('ManufacturerName' in entered_values.keys()) and ('SupplierName' in entered_values.keys()):
            manufacturer_name = (str(entered_values['ManufacturerName'])).upper()
            supplier_name = (str(entered_values['SupplierName'])).lower()
        else:
            return 0

        if (manufacturer_name != '') and (supplier_name != ''):
            man_id = self.obDal.manufacturer_cap(manufacturer_name, supplier_name)
            return man_id
        else:
            return -1

    # NAICS functions
    def ingest_naics_code(self, naics_code, naics_name=''):
        return_id = self.obDal.naics_code_cap(naics_code, naics_name)
        return return_id

    def ingest_naics_codes(self, df_naics_codes):
        ingested_set = []
        self.set_progress_bar('Ingesting NAICS Codes',len(df_naics_codes.index))
        p_bar = 0
        for column, row in df_naics_codes.iterrows():
            naics_code = str(row['NAICSCode'])
            naics_name = str(row['NAICSName'])

            return_id = self.ingest_naics_code(naics_code, naics_name)
            ingested_set.append([return_id, naics_code, naics_name])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def manual_ingest_naics_code(self, atmp_code = '', atmp_name = ''):
        lst_req_fields = [['NAICSCode',45,'This is a numeric value<br>like "32532"',atmp_code,'required'],
                          ['NAICSName',128,'This is the description<br>like "Pesticide and Other Agricultural Chemical Manufacturing (See also 325320.)"',atmp_name,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title='NAICS Code entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('NAICSCode' in entered_values.keys()) and ('NAICSName' in entered_values.keys()):
            naics_code = entered_values['NAICSCode']
            naics_name = entered_values['NAICSName']
        else:
            return 0

        if (naics_code != '') and (naics_name != ''):
            naics_id = self.obDal.naics_code_cap(naics_code, naics_name)
            return naics_id
        else:
            return -1

    # unit of issue symbol functions
    def ingest_uoi_symbol(self, uoi_2_char, ecat_uoi = '', uoi_name = ''):
        return_id = self.obDal.unit_of_issue_symbol_cap(uoi_2_char, uoi_name, ecat_uoi)
        return return_id

    def ingest_uoi_symbols(self, df_uois):
        ingested_set = []
        self.set_progress_bar('Ingesting UOIs Codes',len(df_uois.index))
        p_bar = 0
        for column, row in df_uois.iterrows():
            ecat_uoi = str(row['ECAT UOI'])
            uoi_2_char = str(row['2-Char UOI'])
            uoi_name = str(row['UOI Name'])

            return_id = self.ingest_uoi_symbol(uoi_2_char, ecat_uoi, uoi_name)
            ingested_set.append([return_id, uoi_2_char, ecat_uoi, uoi_name])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def manual_ingest_uois_code(self, atmp_symbol = '', atmp_name = ''):
        lst_req_fields = [['UnitSymbol',2,'This is the 2 character value<br>like "GA"',atmp_symbol,'required'],
                          ['UnitName',45,'This is name<br>like "GALLON"',atmp_name,'required'],
                          ['ECATUnitSymbol',45,'This is different symbol for ecat<br>like "GL"', '','not required']]

        obTextBox = TextBoxObject(lst_req_fields, title='Unit of issue entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('UnitSymbol' in entered_values.keys()) and ('UnitName' in entered_values.keys()) and ('ECATUnitSymbol' in entered_values.keys()):
            uoi_symbol = entered_values['UnitSymbol']
            uoi_name = entered_values['UnitName']
            ecat_symbol = entered_values['ECATUnitSymbol']
        else:
            return 0

        if (uoi_symbol != '') and (uoi_name != '') and (uoi_name != 'not required'):
            uois_id = self.obDal.unit_of_issue_symbol_cap(uoi_symbol, uoi_name)
            return uois_id
        else:
            return -1

    # UNSPSC functions
    def ingest_unspsc(self,unspsc_code,unspsc_title,unspsc_desc=''):
        return_id = self.obDal.unspsc_code_cap(unspsc_code,unspsc_title,unspsc_desc)
        return return_id

    def ingest_unspscs(self,df_unspscs):
        ingested_set = []
        self.set_progress_bar('Ingesting UNSPSCs',len(df_unspscs.index))
        p_bar = 0
        for column, row in df_unspscs.iterrows():
            unspsc_code = str(row['UNSPSCCode'])
            unspsc_title = str(row['UNSPSCName'])[:45]
            unspsc_desc = str(row['UNSPSCDesc'])

            return_id = self.ingest_unspsc(unspsc_code,unspsc_title,unspsc_desc)
            ingested_set.append([return_id,unspsc_code,unspsc_title,unspsc_desc])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set

    def manual_ingest_unspsc_code(self, atmp_unspsc = '', atmp_title = '', atmp_desc = ''):
        lst_req_fields = [['UNSPSC', 45, 'This is the code<br>like "11101705"',atmp_unspsc,'required'],
                          ['UNSPSCTitle', 45, 'This is name<br>like "Aluminum"',atmp_title,'required'],
                          ['UNSPSCDescription', 128, 'This is any other info<br>like "This is aluminum metal"',atmp_desc,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title= 'UNSPSC title entry')
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('UNSPSC' in entered_values.keys()) and ('UNSPSCTitle' in entered_values.keys()) and ('UNSPSCDescription' in entered_values.keys()):
            unspsc = entered_values['UNSPSC']
            unspsc_title = entered_values['UNSPSCTitle']
            unspsc_desc = entered_values['UNSPSCDescription']
        else:
            return 0

        if (unspsc != '') and (unspsc_title != '') and (unspsc_desc != ''):
            unspsc_id = self.obDal.unspsc_code_cap(unspsc, unspsc_title, unspsc_desc)
            return unspsc_id
        else:
            return -1

    # vendor funtions
    def ingest_vendor(self, vendor_code, vendor_name):
        return_id = self.obDal.vendor_cap(vendor_code, vendor_name)
        return return_id

    def ingest_vendors(self, df_vendors):
        ingested_set = []

        self.set_progress_bar('Ingesting Vendors',len(df_vendors.index))
        p_bar = 0
        for column, row in df_vendors.iterrows():

            vendor_name = str(row['VendorName'])
            vendor_name = vendor_name.strip().lower()
            vendor_code = str(row['VendorCode'])

            return_id = self.ingest_vendor(vendor_code, vendor_name)
            ingested_set.append([return_id,vendor_name,vendor_code])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()
        return ingested_set

    def get_vendor_lookup(self):
        df_vendor_lookup = self.obDal.get_vendor_lookup()
        return df_vendor_lookup

    def manual_ingest_vendor(self, atmp_name = '', atmp_code = '',lst_vendor_names=[]):
        lst_req_fields = [['VendorName', 45, 'This is the standard name<br>like "CONSOLIDATED STERILIZER SYSTEMS"', atmp_name,'required'],
                          ['VendorCode', 45, 'This is the not so pretty name<br>like "Consolidated Ster"', atmp_code,'required']]

        obTextBox = TextBoxObject(lst_req_fields, title='Vendor entry',lst_for_dropdown=lst_vendor_names)
        obTextBox.exec()
        entered_values = obTextBox.getReturnSet()

        if ('VendorName' in entered_values.keys()) and ('VendorCode' in entered_values.keys()):
            vendor_name = entered_values['VendorName'].upper()
            vendor_code = entered_values['VendorCode'].upper()
        else:
            return 0

        if (vendor_name != '') and (vendor_code != ''):
            ven_id = self.obDal.vendor_cap(vendor_code, vendor_name)
            return ven_id
        else:
            return -1


    def ingest_uoi_by_symbol(self, unit_of_issue, count, unit_of_measure):
        return_id = -1
        unit_of_issue_id = self.ingest_uoi_symbol(unit_of_issue)
        unit_of_measure_id = self.ingest_uoi_symbol(unit_of_measure)
        if(unit_of_issue_id != -1 and unit_of_measure_id != -1):
            return_id = self.obDal.unit_of_issue_cap(unit_of_issue_id, count, unit_of_measure_id)
        return return_id

    def ingest_uois(self, df_uois):
        ingested_set = []
        self.set_progress_bar('Ingesting UOIs',len(df_uois.index))
        p_bar = 0
        for column, row in df_uois.iterrows():
            return_id = -1
            unit_of_issue = str(row['UnitOfIssue'])
            count = int(row['Count'])
            unit_of_measure = str(row['UnitOfMeasure'])
            if(count > 0):
                return_id = self.ingest_uoi_by_symbol(unit_of_issue, count, unit_of_measure)
            ingested_set.append([return_id, unit_of_issue, count, unit_of_measure])

            p_bar += 1
            self.obProgressBarWindow.update_bar(p_bar)

        self.obProgressBarWindow.close()

        return ingested_set


    def ingest_product(self, newFYCatalogNumber, newManufacturerPartNumber, newIsProductNumberOverride, newProductName, newShortDescription, newLongDescription, newECommerceLongDescription, newCountryOfOriginId, newManufacturerId, newShippingInstructionsId, newRecommendedStorageId, newExpectedLeadTimeId, newCategoryId, newIsControlled=0, newIsDisposable=0, newIsGreen=0, newIsLatexFree=0, newIsRX=0, newIsHazardous=0):
        # if this is the last to join, or if the size has hit the limit, send a runner
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newFYCatalogNumber, newManufacturerPartNumber, newIsProductNumberOverride, newProductName, newShortDescription,
                                               newLongDescription, newECommerceLongDescription,
                                               newCountryOfOriginId, newManufacturerId, newShippingInstructionsId,
                                               newRecommendedStorageId, newExpectedLeadTimeId, newCategoryId, newIsControlled,
                                               newIsDisposable, newIsGreen, newIsLatexFree, newIsRX, newIsHazardous))

            self.obDal.min_product_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newFYCatalogNumber, newManufacturerPartNumber, newIsProductNumberOverride, newProductName, newShortDescription,
                                               newLongDescription, newECommerceLongDescription,
                                               newCountryOfOriginId, newManufacturerId, newShippingInstructionsId,
                                               newRecommendedStorageId, newExpectedLeadTimeId, newCategoryId, newIsControlled,
                                               newIsDisposable, newIsGreen, newIsLatexFree, newIsRX, newIsHazardous))

    def ingest_product_cleanup(self):
        if self.product_collector != []:
            self.obDal.min_product_cap(self.product_collector)

    def set_discon_product_price(self, price_id, is_discontinued):
        # if this is the last to join, or if the size has hit the limit, send a runner
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((price_id, is_discontinued))

            self.obDal.set_discon_product_price(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((price_id, is_discontinued))

    def set_discon_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.set_discon_product_price(self.product_collector)


    def fill_product(self, ProductId, NatoStockNumber='', ModelNumber='', RequiredSampleSize='', NumberOfChannels='', GTIN='', SterilityId=-1, SurfaceTreatmentId=-1, PrecisionId=-1, ProductSEOId=-1, ComponentSetId=-1, FSCCodeId=-1, HazardousCodeId=-1, UNSPSCId=-1, NAICSCodeId=-1, NationalDrugCodeId=-1, ProductWarrantyId=-1, SpeciesId=-1):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((ProductId, NatoStockNumber, ModelNumber, RequiredSampleSize, NumberOfChannels, GTIN, SterilityId, SurfaceTreatmentId, PrecisionId, ProductSEOId, ComponentSetId, FSCCodeId, HazardousCodeId, UNSPSCId, NAICSCodeId, NationalDrugCodeId, ProductWarrantyId, SpeciesId))
            self.obDal.product_fill(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((ProductId, NatoStockNumber, ModelNumber, RequiredSampleSize, NumberOfChannels, GTIN, SterilityId, SurfaceTreatmentId, PrecisionId, ProductSEOId, ComponentSetId, FSCCodeId, HazardousCodeId, UNSPSCId, NAICSCodeId, NationalDrugCodeId, ProductWarrantyId, SpeciesId))

    def fill_product_cleanup(self):
        if self.product_collector != []:
            self.obDal.product_fill(self.product_collector)


    def ingest_shipping_instructions(self, newPackagingDesc, newshippingcode='', newIsFreeShipping=0, newIsColdChain=0):
        return_id = self.obDal.shipping_instructions_cap(newPackagingDesc, newshippingcode, newIsFreeShipping, newIsColdChain)
        return return_id

    def ingest_expected_lead_times(self, expected_lead_time,expedited_lead_time=-1):
        if (expedited_lead_time == -1):
            expedited_lead_time = expected_lead_time
        return_id = self.obDal.lead_time_cap(expected_lead_time,expedited_lead_time)
        return return_id

    def get_fsc_id(self,fsc_code,fsc_code_name=''):
        return_id = self.obDal.get_fsc_id(fsc_code,fsc_code_name)
        return return_id

    def get_unspsc_id(self, unspsc_code,unspsc_code_title=''):
        return_id = self.obDal.get_unspsc_id(unspsc_code,unspsc_code_title)
        return return_id

    def ingest_species(self,species_sci_name, species_name = ''):
        return_id = self.obDal.species_cap(species_sci_name,species_name)
        return return_id


    def ingest_product_price(self, newFyProductNumber,newAllowPurchases,newFyPartNumber,newProductTaxClass,newVendorPartNumber,newIsDiscontinued, newProductId,newVendorId,newUnitOfIssueSymbolId,newUnitOfMeasureSymbolId,newUnitOfIssueQuantity, FyProductNotes):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newFyProductNumber,newAllowPurchases,newFyPartNumber,newProductTaxClass,newVendorPartNumber,newIsDiscontinued,newProductId,newVendorId,newUnitOfIssueSymbolId,newUnitOfMeasureSymbolId,newUnitOfIssueQuantity, FyProductNotes))
            self.obDal.min_product_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newFyProductNumber, newAllowPurchases, newFyPartNumber,
                                                newProductTaxClass, newVendorPartNumber, newIsDiscontinued, newProductId, newVendorId,
                                                newUnitOfIssueSymbolId,newUnitOfMeasureSymbolId,newUnitOfIssueQuantity, FyProductNotes))

    def ingest_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.min_product_price_cap(self.product_collector)

    def fill_product_price(self, is_last, newProductPriceId,newUPC='',newVolume=-1,newWeight=-1,newSize='',newLength=-1,newVariantDesc='',newMinumumFlowTime='',newProfile='',newAmountPriceBreakLevel1=-1,newAmountPriceBreakLevel2=-1,newAmountPriceBreakLevel3=-1,newQuantityPriceBreakLevel1=-1,newQuantityPriceBreakLevel2=-1,newQuantityPriceBreakLevel3=-1,newThicknessId=-1,newHeightId=-1,newDepthId=-1,newWidthId=-1,newCapacityId=-1,newTankCapacityId=-1,newVolumeUnitId=-1,newWeightUnitId=-1,newLengthUnitId=-1,newDimensionsId=-1,newInteriorDimensionsId=-1,newExteriorDimensionsId=-1,newMaterialId=-1,newColorId=-1,newSpeedId=-1,newTubeId=-1,newWeightRangeId=-1,newTemperatureRangeId=-1,newWavelengthId=-1,newWattageId=-1,newVoltageId=-1,newAmperageId=-1,newOuterDiameterId=-1,newInnerDiameterId=-1,newDiameterId=-1,newToleranceId=-1,newAccuracyId=-1,newMassId=-1,newApertureSizeId=-1,newApparelSizeId=-1,newParticleSizeId=-1,newPoreSizeId=-1):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newProductPriceId,newUPC,newVolume,newWeight,newSize,newLength,newVariantDesc,newMinumumFlowTime,newProfile,newAmountPriceBreakLevel1,newAmountPriceBreakLevel2,newAmountPriceBreakLevel3,newQuantityPriceBreakLevel1,newQuantityPriceBreakLevel2,newQuantityPriceBreakLevel3,newThicknessId,newHeightId,newDepthId,newWidthId,newCapacityId,newTankCapacityId,newVolumeUnitId,newWeightUnitId,newLengthUnitId,newDimensionsId,newInteriorDimensionsId,newExteriorDimensionsId,newMaterialId,newColorId,newSpeedId,newTubeId,newWeightRangeId,newTemperatureRangeId,newWavelengthId,newWattageId,newVoltageId,newAmperageId,newOuterDiameterId,newInnerDiameterId,newDiameterId,newToleranceId,newAccuracyId,newMassId,newApertureSizeId,newApparelSizeId,newParticleSizeId,newPoreSizeId))
            self.obDal.product_price_fill(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newProductPriceId,newUPC,newVolume,newWeight,newSize,newLength,newVariantDesc,newMinumumFlowTime,newProfile,newAmountPriceBreakLevel1,newAmountPriceBreakLevel2,newAmountPriceBreakLevel3,newQuantityPriceBreakLevel1,newQuantityPriceBreakLevel2,newQuantityPriceBreakLevel3,newThicknessId,newHeightId,newDepthId,newWidthId,newCapacityId,newTankCapacityId,newVolumeUnitId,newWeightUnitId,newLengthUnitId,newDimensionsId,newInteriorDimensionsId,newExteriorDimensionsId,newMaterialId,newColorId,newSpeedId,newTubeId,newWeightRangeId,newTemperatureRangeId,newWavelengthId,newWattageId,newVoltageId,newAmperageId,newOuterDiameterId,newInnerDiameterId,newDiameterId,newToleranceId,newAccuracyId,newMassId,newApertureSizeId,newApparelSizeId,newParticleSizeId,newPoreSizeId))

    def fill_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.product_price_fill(self.product_collector)

    def ingest_base_price(self, vendor_list_price, fy_discount_percent, fy_cost, estimated_freight, fy_landed_cost, markup_percent_fy_sell, fy_sell_price, markup_percent_fy_list, fy_list_price, ecommerce_discount, is_visible, date_catalog_recieved, catalog_provided_by, product_price_id, newVAProductPriceId=-1, newGSAProductPriceId=-1, newHTMEProductPriceId=-1, newECATProductPriceId=-1, newFEDMALLProductPriceId=-1):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((vendor_list_price, fy_discount_percent, fy_cost, estimated_freight, fy_landed_cost,
                 markup_percent_fy_sell, fy_sell_price, markup_percent_fy_list, fy_list_price, ecommerce_discount,
                 is_visible, date_catalog_recieved, catalog_provided_by, product_price_id,
                 newVAProductPriceId, newGSAProductPriceId, newHTMEProductPriceId, newECATProductPriceId,
                 newFEDMALLProductPriceId))
            self.obDal.base_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((vendor_list_price, fy_discount_percent, fy_cost, estimated_freight, fy_landed_cost, markup_percent_fy_sell, fy_sell_price, markup_percent_fy_list, fy_list_price, ecommerce_discount, is_visible, date_catalog_recieved, catalog_provided_by, product_price_id, newVAProductPriceId, newGSAProductPriceId, newHTMEProductPriceId, newECATProductPriceId, newFEDMALLProductPriceId))

    def ingest_base_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.base_price_cap(self.product_collector)




    def ecat_product_price_cap(self, newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newECATPricingApproved,
                               newECATApprovedPriceDate, newECATSellPrice, newECATMaxMarkup):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newECATPricingApproved,
                               newECATApprovedPriceDate, newECATSellPrice, newECATMaxMarkup))
            self.obDal.ecat_product_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newECATPricingApproved,
                               newECATApprovedPriceDate, newECATSellPrice, newECATMaxMarkup))

    def ingest_ecat_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.ecat_product_price_cap(self.product_collector)


    def fedmall_product_price_cap(self,newIsVisible, newDateCatalogReceived, newFEDMALLSellPrice, newFEDMALLApprovedPriceDate , newFEDMALLPricingApproved, newFEDMALLContractNumber, newFEDMALLContractModificationNumber, newFEDMALLProductGMPercent, newFEDMALLProductGMPrice):
        return_id = self.obDal.fedmall_product_price_cap(newIsVisible, newDateCatalogReceived, newFEDMALLSellPrice, newFEDMALLApprovedPriceDate, newFEDMALLPricingApproved, newFEDMALLContractNumber, newFEDMALLContractModificationNumber, newFEDMALLProductGMPercent, newFEDMALLProductGMPrice)
        return return_id


    def gsa_product_price_cap(self, newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice,
                              newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                              newContractNumber, newContractModificatactionNumber, newGSAPricingApproved,
                              newGSAApprovedPriceDate, newApprovedPercent, newGSABasePrice, newGSASellPrice,
                              newMFCPercent, newMFCPrice, newGSA_SIN):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append(
                (newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice, newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber, newContractNumber, newContractModificatactionNumber, newGSAPricingApproved, newGSAApprovedPriceDate, newApprovedPercent, newGSABasePrice, newGSASellPrice, newMFCPercent, newMFCPrice, newGSA_SIN))
            self.obDal.gsa_product_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice, newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber, newContractNumber, newContractModificatactionNumber, newGSAPricingApproved, newGSAApprovedPriceDate, newApprovedPercent, newGSABasePrice, newGSASellPrice, newMFCPercent, newMFCPrice, newGSA_SIN))

    def ingest_gsa_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.gsa_product_price_cap(self.product_collector)


    def htme_product_price_cap(self, newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newHTMEPricingApproved,
                               newHTMEApprovedPriceDate, newHTMESellPrice, newHTMEMaxMarkup):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newHTMEPricingApproved,
                               newHTMEApprovedPriceDate, newHTMESellPrice, newHTMEMaxMarkup))
            self.obDal.htme_product_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract,
                               newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber,
                               newContractNumber, newContractModificatactionNumber, newHTMEPricingApproved,
                               newHTMEApprovedPriceDate, newHTMESellPrice, newHTMEMaxMarkup))

    def ingest_htme_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.htme_product_price_cap(self.product_collector)


    def va_product_price_cap(self, newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice, newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber, newContractNumber, newContractModificatactionNumber, newVAPricingApproved, newVAApprovedPriceDate, newApprovedPercent, newVABasePrice, newVASellPrice, newMFCPercent, newMFCPrice, newVA_SIN):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice, newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber, newContractNumber, newContractModificatactionNumber, newVAPricingApproved, newVAApprovedPriceDate, newApprovedPercent, newVABasePrice, newVASellPrice, newMFCPercent, newMFCPrice, newVA_SIN))
            self.obDal.va_product_price_cap(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((newBaseProductPriceId, newFyProductNumber, newOnContract, newApprovedBasePrice, newApprovedSellPrice, newApprovedListPrice, newContractedManufacturerPartNumber, newContractNumber, newContractModificatactionNumber, newVAPricingApproved, newVAApprovedPriceDate, newApprovedPercent, newVABasePrice, newVASellPrice, newMFCPercent, newMFCPrice, newVA_SIN))

    def ingest_va_product_price_cleanup(self):
        if self.product_collector != []:
            self.obDal.va_product_price_cap(self.product_collector)


    def set_product_notes(self,ProductPriceId, FyProductNotes):
        if (len(self.product_notes_collector) > self.load_limit):
            self.product_notes_collector.append((ProductPriceId, FyProductNotes))
            self.obDal.set_product_notes(self.product_notes_collector)
            self.product_notes_collector = []
        else:
            self.product_notes_collector.append((ProductPriceId, FyProductNotes))

    def set_product_notes_cleanup(self):
        if self.product_notes_collector != []:
            self.obDal.set_product_notes(self.product_notes_collector)


    def set_productimage(self, product_id, product_image_url, object_name, image_preference, image_caption, image_width, image_height):
        if (len(self.product_collector) > self.load_limit):
            self.product_collector.append((product_id, product_image_url, object_name, image_preference, image_caption, image_width, image_height))
            self.obDal.product_image_capture(self.product_collector)
            self.product_collector = []
        else:
            self.product_collector.append((product_id, product_image_url, object_name, image_preference, image_caption, image_width, image_height))

    def set_productimage_cleanup(self):
        if self.product_collector != []:
            self.obDal.product_image_capture(self.product_collector)


    def set_productdocument_cap(self, ProductId, ProductDocumentUrl, ProductDocumentName, ProductDocumentType, ProductDocumentPreference = 0):
        if (len(self.product_document_collector) > self.load_limit):
            self.product_document_collector.append((ProductId, ProductDocumentUrl, ProductDocumentName, ProductDocumentType, ProductDocumentPreference))
            self.obDal.productdocument_cap(self.product_document_collector)
            self.product_document_collector = []

        else:
            self.product_document_collector.append((ProductId, ProductDocumentUrl, ProductDocumentName, ProductDocumentType, ProductDocumentPreference))

    def set_productdocument_cleanup(self):
        if self.product_document_collector != []:
            self.obDal.productdocument_cap(self.product_document_collector)


    def set_productvideo_cap(self, product_id, video_path, video_caption, video_preference = 0):
        if (len(self.product_video_collector) > self.load_limit):
            self.product_video_collector.append((product_id, video_path, video_caption, video_preference))
            self.obDal.productvideo_cap(self.product_video_collector)
            self.product_video_collector = []

        else:
            self.product_video_collector.append((product_id, video_path, video_caption, video_preference))

    def set_productvideo_cleanup(self):
        if self.product_video_collector != []:
            self.obDal.productvideo_cap(self.product_video_collector)


    def set_bc_update_toggles(self, price_id, fy_product_number, price_toggle, data_toggle):
        if (len(self.product_bc_toggle_collector) > self.load_limit):
            self.product_bc_toggle_collector.append((price_id, fy_product_number, price_toggle, data_toggle))
            self.obDal.set_bc_toggles(self.product_bc_toggle_collector)
            self.product_bc_toggle_collector = []

        else:
            self.product_bc_toggle_collector.append((price_id, fy_product_number, price_toggle, data_toggle))

    def set_bc_update_toggles_cleanup(self):
        if self.product_bc_toggle_collector != []:
            self.obDal.set_bc_toggles(self.product_bc_toggle_collector)


    def set_is_discon_allow_purchase(self, price_id, fy_product_number, is_discontinued, allow_purchases):
        if (len(self.product_discon_collector) > self.load_limit):
            self.product_discon_collector.append((price_id, fy_product_number, is_discontinued, allow_purchases))
            self.obDal.set_discon(self.product_discon_collector)
            self.product_discon_collector = []

        else:
            self.product_discon_collector.append((price_id, fy_product_number, is_discontinued, allow_purchases))

    def set_is_discon_allow_purchase_cleanup(self):
        if self.product_discon_collector != []:
            self.obDal.set_discon(self.product_discon_collector)


    def set_is_visible(self, base_id, is_visible):
        if (len(self.product_is_visible_collector) > self.load_limit):
            self.product_is_visible_collector.append((base_id, is_visible))
            self.obDal.set_is_visible(self.product_is_visible_collector)
            self.product_is_visible_collector = []

        else:
            self.product_is_visible_collector.append((base_id, is_visible))

    def set_is_visible_cleanup(self):
        if self.product_is_visible_collector != []:
            self.obDal.set_is_visible(self.product_is_visible_collector)


    def set_update_asset(self, product_id, update_asset):
        if (len(self.product_update_asset_collector) > self.load_limit):
            self.product_update_asset_collector.append((product_id, update_asset))
            self.obDal.set_update_asset(self.product_update_asset_collector)
            self.product_update_asset_collector = []

        else:
            self.product_update_asset_collector.append((product_id, update_asset))

    def set_update_asset_cleanup(self):
        if self.product_update_asset_collector != []:
            self.obDal.set_update_asset(self.product_update_asset_collector)

    def set_ecat_toggles(self,base_id, fy_product_number, ecat_contract, ecat_approved):
        if (len(self.product_ecat_toggle_collector) > self.load_limit):
            self.product_ecat_toggle_collector.append((base_id, fy_product_number, ecat_contract, ecat_approved))
            self.obDal.set_ecat_toggles(self.product_ecat_toggle_collector)
            self.product_ecat_toggle_collector = []

        else:
            self.product_ecat_toggle_collector.append((base_id, fy_product_number, ecat_contract, ecat_approved))

    def set_ecat_toggles_cleanup(self):
        if self.product_ecat_toggle_collector != []:
            self.obDal.set_ecat_toggles(self.product_ecat_toggle_collector)


    def set_htme_toggles(self,base_id, fy_product_number, htme_contract, htme_approved):
        if (len(self.product_htme_toggle_collector) > self.load_limit):
            self.product_htme_toggle_collector.append((base_id, fy_product_number, htme_contract, htme_approved))
            self.obDal.set_htme_toggles(self.product_htme_toggle_collector)
            self.product_htme_toggle_collector = []

        else:
            self.product_htme_toggle_collector.append((base_id, fy_product_number, htme_contract, htme_approved))

    def set_htme_toggles_cleanup(self):
        if self.product_htme_toggle_collector != []:
            self.obDal.set_htme_toggles(self.product_htme_toggle_collector)


    def set_gsa_toggles(self,base_id, fy_product_number, gsa_contract, gsa_approved):
        if (len(self.product_gsa_toggle_collector) > self.load_limit):
            self.product_gsa_toggle_collector.append((base_id, fy_product_number, gsa_contract, gsa_approved))
            self.obDal.set_gsa_toggles(self.product_gsa_toggle_collector)
            self.product_gsa_toggle_collector = []

        else:
            self.product_gsa_toggle_collector.append((base_id, fy_product_number, gsa_contract, gsa_approved))

    def set_gsa_toggles_cleanup(self):
        if self.product_gsa_toggle_collector != []:
            self.obDal.set_gsa_toggles(self.product_gsa_toggle_collector)


    def set_va_toggles(self,base_id, fy_product_number, va_contract, va_approved):
        if (len(self.product_va_toggle_collector) > self.load_limit):
            self.product_va_toggle_collector.append((base_id, fy_product_number, va_contract, va_approved))
            self.obDal.set_va_toggles(self.product_va_toggle_collector)
            self.product_va_toggle_collector = []

        else:
            self.product_va_toggle_collector.append((base_id, fy_product_number, va_contract, va_approved))

    def set_va_toggles_cleanup(self):
        if self.product_va_toggle_collector != []:
            self.obDal.set_va_toggles(self.product_va_toggle_collector)


## end ##