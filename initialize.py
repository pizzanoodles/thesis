
import pandas as pd
import os


def initialize_dir_region():
    dict_reg = {'value': ['NCR', 'CAR', 'Region 1', 'Region 2', 'Region 3', 'Region 4A', 'Region 4B', 'Region 5', 'Region 6', 'Region 7', 'Region 8', 'Region 9', 'Region 10', 'Region 11', 'Region 12', 'Region 13', 'BARMM', 'NIR'], 'label': [
        'NCR', 'CAR', 'Region I', 'Region II', 'Region III', 'Region IV-A', 'Region IV-B', 'Region V', 'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X', 'Region XI', 'Region XII', 'Region XIII', 'BARMM', 'NIR']}
    return dict_reg


def get_cities(reg, yr, dt, page):
    link_init = "SCBAA/" + yr + "/" + reg + ".xlsx"
    sheets = pd.ExcelFile(link_init)
    cities = sheets.sheet_names
    for c in cities:
        sum = 0
        city_init = pd.read_excel(link_init, c)
        if(dt == "Revenue"):
            sum = city_init.iloc[35, 4]
        elif(dt == "Appropriations"):
            sum = city_init.iloc[110, 4]
        if(sum == 0 and page == "datavis"):
            cities.remove(c)
    return cities


def initialize_dir_year():
    ROOT_DIR = os.path.abspath(os.curdir)
    rootdir = ROOT_DIR + "/SCBAA"
    directory_contents = os.listdir(rootdir)
    init_list = list(directory_contents)
    for item in init_list:
        if(os.path.isfile(rootdir+"/"+item)):
            directory_contents.remove(item)
    directory_contents.sort()
    return directory_contents


def get_allapptype(r, c):
    label = []
    value = []
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Appropriations")):
        label.append(
            "&nbsp;&nbsp;• Current Appropriations")
        value.append("Curr. Appropriations")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. General Public Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ General Public Services")
        value.append("Curr. General Public Services")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Education")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Education")
        value.append("Curr. Education")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Health Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Health, Nutrition, and Population Control")
        value.append("Curr. Health Services")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Labor and Employment")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Labor and Employment")
        value.append("Curr. Labor and Employment")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Housing")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Housing and Community Development")
        value.append("Curr. Housing")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Social Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Social Services and Social Welfare")
        value.append("Curr. Social Services")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Economic Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Economic Services")
        value.append("Curr. Economic Services")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Other Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Other Services Sector")
        value.append("Curr. Other Services")
    if checklst_items(get_amountallyr(r, c, lbl="Curr. Other Purposes")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Other Purposes")
        value.append("Curr. Other Purposes")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Appropriations")):
        label.append(
            "&nbsp;&nbsp;• Continuing Appropriations")
        value.append("Cont. Appropriations")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. General Public Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ General Public Services")
        value.append("Cont. General Public Services")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Education")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Education")
        value.append("Cont. Education")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Health Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Health, Nutrition, and Population Control")
        value.append("Cont. Health Services")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Labor and Employment")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Labor and Employment")
        value.append("Cont. Labor and Employment")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Housing")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Housing and Community Development")
        value.append("Cont. Housing")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Social Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Social Services and Social Welfare")
        value.append("Cont. Social Services")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Economic Services")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Economic Services")
        value.append("Cont. Economic Services")
    if checklst_items(get_amountallyr(r, c, lbl="Cont. Other Purposes")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Other Purposes")
        value.append("Cont. Other Purposes")
    return label, value


def get_allrevtype(r, c):
    label = []
    value = []
    if checklst_items(get_amountallyr(r, c, lbl="Local Sources")):
        label.append(
            "&nbsp;&nbsp;• Local Sources")
        value.append("Local Sources")
    if checklst_items(get_amountallyr(r, c, lbl="Tax Revenues")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Tax Revenues")
        value.append("Tax Revenues")
    if checklst_items(get_amountallyr(r, c, lbl="Non-Tax Revenues")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Non-Tax Revenues")
        value.append("Non-Tax Revenues")
    if checklst_items(get_amountallyr(r, c, lbl="External Sources")):
        label.append(
            "&nbsp;&nbsp;• External Sources")
        value.append("External Sources")
    if checklst_items(get_amountallyr(r, c, lbl="National Internal Revenue Taxes")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Share from the National Internal Revenue Taxes (IRA)")
        value.append("National Internal Revenue Taxes")
    if checklst_items(get_amountallyr(r, c, lbl="GOCCs")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Share from GOCCs")
        value.append("GOCCs")
    if checklst_items(get_amountallyr(r, c, lbl="National Tax Collections")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Shares from National Tax Collections")
        value.append("National Tax Collections")
    if checklst_items(get_amountallyr(r, c, lbl="Other Receipts")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Other Receipts")
        value.append("Other Receipts")
    if checklst_items(get_amountallyr(r, c, lbl="Inter-local Transfer")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Inter-local Transfer")
        value.append("Inter-local Transfer")
    if checklst_items(get_amountallyr(r, c, lbl="Capital/Investment Receipts")):
        label.append(
            "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;◦ Capital/Investment Receipts")
        value.append("Capital/Investment Receipts")
    if checklst_items(get_amountallyr(r, c, lbl="Receipts from Borrowings")):
        label.append(
            "&nbsp;&nbsp;• Receipts from Borrowings")
        value.append("Receipts from Borrowings")
    return label, value


def checklst_items(lst):
    cleanedList = [x for x in lst if x != 0]
    if len(cleanedList) > 1:
        return True
    else:
        return False


def get_amountallyr(r, c, lbl):
    year = initialize_dir_year()
    locals = []
    for y in year:
        link_init = "SCBAA/" + y + "/" + r + ".xlsx"
        reg_init = pd.ExcelFile(link_init)
        city_init = pd.read_excel(reg_init, c)
        total = find_typedata(city_init, lbl)
        locals.append(total)
    return locals


def find_typedata(city_init, lbl):
    if(lbl == "Local Sources"):
        total = get_localsources(city_init)
    elif(lbl == "Tax Revenues"):
        total = get_taxrevenues(city_init)
    elif(lbl == "Non-Tax Revenues"):
        total = get_nontaxrevenues(city_init)
    elif(lbl == "External Sources"):
        total = get_externalrevenues(city_init)
    elif(lbl == "National Internal Revenue Taxes"):
        total = get_nirat(city_init)
    elif(lbl == "GOCCs"):
        total = get_gocc(city_init)
    elif(lbl == "National Tax Collections"):
        total = get_ntc(city_init)
    elif(lbl == "Other Receipts"):
        total = get_or(city_init)
    elif(lbl == "Inter-local Transfer"):
        total = get_interl(city_init)
    elif(lbl == "Capital/Investment Receipts"):
        total = get_cir(city_init)
    elif(lbl == "Receipts from Borrowings"):
        total = get_rb(city_init)
    elif(lbl == "Curr. Appropriations"):
        total = get_currapp(city_init)
    elif(lbl == "Curr. General Public Services"):
        total = get_currgps(city_init)
    elif(lbl == "Curr. Education"):
        total = get_curredu(city_init)
    elif(lbl == "Curr. Health Services"):
        total = get_currheal(city_init)
    elif(lbl == "Curr. Labor and Employment"):
        total = get_currlab(city_init)
    elif(lbl == "Curr. Housing"):
        total = get_currhous(city_init)
    elif(lbl == "Curr. Social Services"):
        total = get_currsoc(city_init)
    elif(lbl == "Curr. Economic Services"):
        total = get_curreco(city_init)
    elif(lbl == "Curr. Other Services"):
        total = get_currotherss(city_init)
    elif(lbl == "Curr. Other Purposes"):
        total = get_currothersp(city_init)
    elif(lbl == "Cont. Appropriations"):
        total = get_contapp(city_init)
    elif(lbl == "Cont. General Public Services"):
        total = get_contgps(city_init)
    elif(lbl == "Cont. Education"):
        total = get_contedu(city_init)
    elif(lbl == "Cont. Health Services"):
        total = get_contheal(city_init)
    elif(lbl == "Cont. Labor and Employment"):
        total = get_contlab(city_init)
    elif(lbl == "Cont. Housing"):
        total = get_conthous(city_init)
    elif(lbl == "Cont. Social Services"):
        total = get_contsoc(city_init)
    elif(lbl == "Cont. Economic Services"):
        total = get_conteco(city_init)
    elif(lbl == "Cont. Other Purposes"):
        total = get_contothers(city_init)
    elif(lbl == "Total Appropriations"):
        total = get_totalapp(city_init)
    elif(lbl == "Total Revenues"):
        total = get_totalrev(city_init)
    return total


def get_totalrev(city_init):
    total_rev = city_init.iloc[35, 4]
    return total_rev


def get_totalapp(city_init):
    total_app = city_init.iloc[110, 4]
    return total_app


def get_currapp(city_init):
    tr = city_init.iloc[91, 4]
    return tr


def get_currgps(city_init):
    tr = city_init.iloc[40:43, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_curredu(city_init):
    tr = city_init.iloc[44:47, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currheal(city_init):
    tr = city_init.iloc[48:51, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currlab(city_init):
    tr = city_init.iloc[52:55, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currhous(city_init):
    tr = city_init.iloc[56:59, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currsoc(city_init):
    tr = city_init.iloc[60:63, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_curreco(city_init):
    tr = city_init.iloc[64:67, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currotherss(city_init):
    tr = city_init.iloc[68:71, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_currothersp(city_init):
    tr = city_init.iloc[73:91, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_contapp(city_init):
    tr = city_init.iloc[109, 4]
    return tr


def get_contgps(city_init):
    tr = city_init.iloc[94, 4]
    return tr


def get_contedu(city_init):
    tr = city_init.iloc[96, 4]
    return tr


def get_contheal(city_init):
    tr = city_init.iloc[98, 4]
    return tr


def get_contlab(city_init):
    tr = city_init.iloc[100, 4]
    return tr


def get_conthous(city_init):
    tr = city_init.iloc[102, 4]
    return tr


def get_contsoc(city_init):
    tr = city_init.iloc[104, 4]
    return tr


def get_conteco(city_init):
    tr = city_init.iloc[106, 4]
    return tr


def get_contothers(city_init):
    tr = city_init.iloc[108, 4]
    return tr


def get_localsources(city_init):
    tr = city_init.iloc[12, 4]
    ntr = city_init.iloc[17, 4]
    total = tr+ntr
    return total


def get_taxrevenues(city_init):
    tr = city_init.iloc[12, 4]
    return tr


def get_nontaxrevenues(city_init):
    ntr = city_init.iloc[17, 4]
    return ntr


def get_externalrevenues(city_init):
    tr = city_init.iloc[19:34, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_nirat(city_init):
    tr = city_init.iloc[19, 4]
    return tr


def get_gocc(city_init):
    tr = city_init.iloc[20, 4]
    return tr


def get_ntc(city_init):
    tr = city_init.iloc[22:26, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_or(city_init):
    tr = city_init.iloc[27:29, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_interl(city_init):
    tr = city_init.iloc[29, 4]
    return tr


def get_cir(city_init):
    tr = city_init.iloc[31:34, 4]
    cleanedList = [x for x in tr if str(x) != 'nan']
    return sum(cleanedList)


def get_rb(city_init):
    tr = city_init.iloc[34, 4]
    return tr


def get_actualbel(data):
    label = ""
    if(data == "Curr. Appropriations"):
        label = "Current Appropriations"
    elif(data == "Curr. General Public Services" or data == "Cont. General Public Services"):
        label = "General Public Services"
    elif(data == "Curr. Education" or data == "Cont. Education"):
        label = "Education"
    elif(data == "Curr. Health Services" or data == "Cont. Health Services"):
        label = "Health, Nutrition and Population Control"
    elif(data == "Curr. Labor and Employment" or data == "Cont. Labor and Employment"):
        label = "Labor and Employment"
    elif(data == "Curr. Housing" or data == "Cont. Housing"):
        label = "Housing and Community Development"
    elif(data == "Curr. Social Services" or data == "Cont. Social Services"):
        label = "Social Services and Social Welfare"
    elif(data == "Curr. Economic Services" or data == "Cont. Economic Services"):
        label = "Economic Services"
    elif(data == "Curr. Other Services"):
        label = "Other Services Sector"
    elif(data == "Curr. Other Purposes" or data == "Cont. Other Purposes"):
        label = "Other Purposes"
    elif(data == "Cont. Appropriations"):
        label = "Continuing Appropriations"
    else:
        label = data

    return label


def get_definition(data):
    ###SOURCE LARGEST###
    definition = ""
    # REVENUES
    if(data == "Total Revenues"):
        definition = "The full amount of the total revenues garnered"
    elif(data == "Local Sources"):
        definition = "Revenue garnered from inside the Local Government Unit"
    elif(data == "External Sources"):
        definition = "Revenue garnered from outside the Local Government Unit"
    elif(data == "Receipts from Borrowings"):
        definition = "Money from loans/borrowings from both internal/external sources"
    elif(data == "Tax Revenues"):
        definition = "Revenue from various local taxes"
    elif(data == "Non-Tax Revenues"):
        definition = "Revenue from non-tax sources"
    elif(data == "Share from the National Internal Revenue Taxes (IRA)"):
        definition = "Administered by the BIR. Income, Indirect, Excise, and Stamp Taxes"
    elif(data == "Share from GOCCs"):
        definition = "Revenue from Government Owned Controlled Corporation"
    elif(data == "Other Shares from National Tax Collections"):
        definition = "Revenue from Government Owned Controlled Corporation"
    elif(data == "Other Receipts"):
        definition = "Other Revenues from financial transactions of the Local Government Unit"
    elif(data == "Inter-local Transfer"):
        definition = "Revenues from other government levels to help the LGU's development"
    elif(data == "Capital/Investment Receipts"):
        definition = "Various revenues from investments and capital assets"
    elif(data == "Tax Revenue - Property"):
        definition = "Real estate tax from properties of individuals/corporations"
    elif(data == "Tax Revenue - Goods and Services"):
        definition = "Value-added tax levied on most goods and services sold for domestic consumption"
    elif(data == "Other Local Taxes"):
        definition = "Various taxes from government services"
    elif(data == "Service Income"):
        definition = "Income gained from various government Services"
    elif(data == "Business Income"):
        definition = "Income gained from various government Businesses"
    elif(data == "Other Income and Receipts"):
        definition = "Other sources of income from various sales"
    elif(data == "Share from Ecozone"):
        definition = "Revenue from Special Economic Zones(SEZ), an area in a country that is subject to different economic regulations than other regions within the same country"
    elif(data == "Share from EVAT"):
        definition = "Revenue from Extended Value added Taxes"
    elif(data == "Share from National Wealth"):
        definition = "Local Government's share from the National Government's revenues"
    elif(data == "Share from Tobacco Excise Tax"):
        definition = "Tax from Tobacco based products"
    elif(data == "Grants and Donations"):
        definition = "Various grants and donations provided to the local government"
    elif(data == "Other Subsidy Income"):
        definition = "Grants of money granted to the government or a public body to assist on a certain service"
    elif(data == "Sale of Capital Assets"):
        definition = "Revenue from sale of a government owned investment item for government purposes"
    elif(data == "Sale of Investments"):
        definition = "Revenue from return of investments"
    elif(data == "Proceeds from Collections of Loans Receivable"):
        definition = "Revenue garnered from the collection of various loans"
    # TOTAL APPROPRIATIONS
    elif(data == "Total Appropriations"):
        definition = "The full amount of the budget expended"
    elif(data == "Current Appropriations"):
        definition = "Budget that is set aside for various government uses for this current year"
    elif(data == "Continuing Appropriations"):
        definition = "Appropriations available to support obligations for a specified purpose or project, even when these obligations are incurred beyond the budget year"
    elif(data == "General Public Services"):
        definition = "Budget for General Services that the government provide to the public"
    elif(data == "Education"):
        definition = "Budget for education related purposes, (schools,seminars, etc.)"
    elif(data == "Health, Nutrition and Population Control"):
        definition = "Budget for public's health-related expenses."
    elif(data == "Labor and Employment"):
        definition = "Budget for the public's employment related expenses"
    elif(data == "Housing and Community Development"):
        definition = "Budget for the public's local housing development expenses"
    elif(data == "Social Services and Social Welfare"):
        definition = "Budget for aiding disadvantaged, distressed, or vulnerable persons or groups."
    elif(data == "Economic Services"):
        definition = "Budget for economic utility expenses"
    elif(data == "Other Services Sector"):
        definition = "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)"
    elif(data == "Other Purposes"):
        definition = "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)"
    elif(data == "Others"):
        definition = "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)"
    elif(data == "Debt Service"):
        definition = "Budget for payment and repayment of principal capital"
    elif(data == "LDRRMF"):
        definition = "Budget invested in disaster risk reductions"
    elif(data == "20% Development Fund"):
        definition = "Budget used for expenses in the development of the local government"
    elif(data == "Share from National Wealth"):
        definition = "Expenses made for share in the National Wealth"
    elif(data == "Allocation for Senior Citizens and PWD"):
        definition = "Budget for expenses used for the programs, projects and activities proportionately divided among senior citizens and persons with disability"
    elif(data == "Financial Expense"):
        definition = "Expenses associated with financing the certain sector."
    elif(data == "Amortization"):
        definition = "Budget for specifically repaying of debts."
    elif(data == "Personnel Services"):
        definition = "Budget for expenses on the personnel (salaries, wages, and other compensation)"
    elif(data == "Maintenance and Other Operating Expenses"):
        definition = "Budget for the expenses made for regulation of an operation of a sector."

    elif(data == "Capital Outlay"):
        definition = "Budget for expenses made to acquire capital assets to be used for a certain sector."
    else:
        definition = "Budget for services not classified in other sectors. (Repairs of equipment, promotions, etc.)"

    return definition
