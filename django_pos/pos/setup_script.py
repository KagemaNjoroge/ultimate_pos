from company.models import Company, Branch
from products.models import TaxGroup


def create_demo_company():
    company = Company.objects.create(
        phone_number="1234567890",
        email="demo@company.com",
        city="Demo City",
        address="123 Demo Street",
        company_name="Demo Company",
        currency_symbol="KES",
        tax_registration_number="P012345678H",
    )
    return company


def create_demo_branch(company: Company):
    branch = Branch.objects.create(
        company=company,
        branch_name="Demo Branch",
        phone_number="0987654321",
        email="demobranch@company.com",
        address="456 Demo Avenue",
        is_headquarter=True,
    )
    return branch


def setup_tax_groups():
    """

    There are two (2) tax rates:-

    16% (General rate) - this rate applies to all taxable goods and taxable services other than zero-rated supplies.
    0% (Zero-rate) - this rate applies to specific supplies listed in the Second Schedule to the VAT Act, 2013.

    Note: 8% (Other rate) - This rate applied to certain supplies (petroleum products) prior to 1st July 2023
    but was deleted by the Finance Act, 2023.

    Exempt supplies are not taxable supplies and any related input tax is therefore not deductible.
    Exempt supplies are listed in the First Schedule to the VAT Act 2013. Taxpayers who only make exempt
    supplies are not required to register for VAT.

    """
    tax_groups = [
        {
            "name": "General Rate",
            "tax_rate": 16.0,
            "status": "ACTIVE",
            "description": "This rate applies to all taxable goods and taxable services other than zero-rated supplies.",
        },
        {
            "name": "Zero Rate",
            "tax_rate": 0.0,
            "status": "ACTIVE",
            "description": """Zero-rated supplies are taxable supplies on which the tax rate is 0%. 
            Zero-rated supplies are listed in the Second Schedule to the VAT Act, 2013. 
            Taxpayers who only make zero-rated supplies are not required to register for VAT.""",
        },
        {
            "name": "Exempt",
            "tax_rate": 0.0,
            "status": "ACTIVE",
            "description": """Exempt supplies are not taxable supplies and any related input tax is therefore not deductible.
              Exempt supplies are listed in the First Schedule to the VAT Act 2013. 
              Taxpayers who only make exempt supplies are not required to register for VAT.""",
        },
        {
            "name": "Other Rate",
            "tax_rate": 8.0,
            "status": "INACTIVE",
            "description": """This rate applied to certain supplies (petroleum products) 
            prior to 1st July 2023 but was deleted by the Finance Act, 2023.""",
        },
    ]
    for tax_group in tax_groups:
        TaxGroup.objects.get_or_create(
            name=tax_group["name"],
            defaults={
                "tax_rate": tax_group["tax_rate"],
                "status": tax_group["status"],
                "description": tax_group["description"],
            },
        )
    return TaxGroup.objects.all()


if __name__ == "__main__":
    company = create_demo_company()
    branch = create_demo_branch(company)
    tax_groups = setup_tax_groups()

    tax_groups = [tax_group.name for tax_group in tax_groups]
    print(
        f"Demo company '{company.company_name}' and branch '{branch.branch_name}' created with tax groups: {tax_groups}"
    )
