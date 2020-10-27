from manager.models import SupplierOrderedTextile, SupplierOrderedCornice

def GetTextileQuantity(start, end):
    textile_mass = {}
    qs = SupplierOrderedTextile.objects.filter(date_created__gte=start, date_created__lte=end)
    for q in qs:
        mass = {}
        textile = f'{q.item.item.collection} {q.item.item.model} {q.item.item.color}'
        quantity = q.item.quantity
        manufacturer = q.item.item.manufacturer.name
        if manufacturer in textile_mass:
            if textile in textile_mass[manufacturer]:
                textile_mass[manufacturer][textile] += quantity
            else:
                textile_mass[manufacturer][textile] = quantity
        else:
            mass[textile] = quantity
            textile_mass[manufacturer] = mass

    textile_mass_sort = {}
    for q in textile_mass:
        mass = {k: v for k, v in sorted(textile_mass[q].items(), key=lambda item: item[1], reverse=True)}
        textile_mass_sort[q] = mass
    return textile_mass_sort

def GetCorniceQuantity(start, end):
    cornice_mass = {}
    qc = SupplierOrderedCornice.objects.filter(date_created__gte=start, date_created__lte=end)
    for q in qc:
        mass = {}
        textile = f'{q.item.item.collection} {q.item.item.model} {q.item.item.long}'
        quantity = q.item.quantity
        manufacturer = q.item.item.manufacturer.name
        if manufacturer in cornice_mass:
            if textile in cornice_mass[manufacturer]:
                cornice_mass[manufacturer][textile] += quantity
            else:
                cornice_mass[manufacturer][textile] = quantity
        else:
            mass[textile] = quantity
            cornice_mass[manufacturer] = mass

    cornice_mass_sort = {}
    for q in cornice_mass:
        mass = {k: v for k, v in sorted(cornice_mass[q].items(), key=lambda item: item[1], reverse=True)}
        cornice_mass_sort[q] = mass
    return cornice_mass_sort
