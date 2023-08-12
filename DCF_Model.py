import argparse

#Calling Argument Parser
CLI = argparse.ArgumentParser()

CLI.add_argument(
    "--FCF", #name on the CLI, drop the '--' for the positional/required parameters
    help='Test',
    nargs="*", #0 or more values expected ==> creates a list
    type=int,
    default = [100,105,200,105,130], #default if nothing is provided
)
CLI.add_argument(
    "--RF",
    type = float,
    default = 3
)
CLI.add_argument(
    "--TGR",
    type = float,
    default = 2.5
)
CLI.add_argument(
    "--Beta",
    type = float,
    default = 1
)
CLI.add_argument(
    "--ERP",
    type = float,
    default = 7
)
args = CLI.parse_args()

def main():
    """
    Following variables are used: \n
    FCF : Free Cash Flows, entered as numbers with spaces, this argument takes n FCFs
    ERP : Equity Risk Premium
    Beta : Sensitivity to market return
    TGR : Terminal Growth Rate
    Risk Free Rate: Risk Free Rate used in CAPM to determine
    """
    #Calling DCF model
    Discount_Cash_Flows = DCF(args.FCF)

    #Calling TV model
    Discount_Terminal_Value = TV(args.FCF,args.TGR,CAPM(args.Beta,args.RF,args.ERP))

    Total_Value = sum(Discount_Cash_Flows)+Discount_Terminal_Value

    print(f'Total Value of Equity: {Total_Value}')

def CAPM(beta,rf,equity_risk_premium):
    """This function generates the cost of equity
    from the CAPM model which is used as the discount rate"""

    coe = args.RF + (args.Beta * args.ERP)

    return coe/100

def DCF(fcf):

    print(f'There are {len(args.FCF)} years of free cash flow')

    #calling CAPM model to derive coe
    coe = CAPM(args.Beta,args.RF,args.ERP)
    print(f'Cost of equity is:\n {coe}')

    discount_cash_flows = [ f / (1+(coe/100))**(i+1) for i , f in enumerate(fcf)]

    print(f'Sum of discounted cash flows: {sum(discount_cash_flows)}')

    return discount_cash_flows

def TV(fcf,tgr,coe):

    #Terminal Value Using Final Year of Cash Flow
    print(f'The final year of Free Cash Flow being used for TV is: {fcf[-1]}')

    #TV
    terminal_value = (fcf[-1] * (1+(tgr/100))/(coe-(tgr/100)))

    #Discount TV
    discount_terminal_value = (terminal_value) / (1+coe) **(len(fcf))

    print(f'The Terminal Value is: {terminal_value} \n Discount TV: {discount_terminal_value}')

    return discount_terminal_value

if __name__ == "__main__":
    print(main.__doc__)
    main()

