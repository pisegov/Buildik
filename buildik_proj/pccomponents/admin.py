from django.contrib import admin
import pccomponents.models as pcc

@admin.register(pcc.CPU, pcc.GPU, pcc.Motherboard, 
                pcc.RAM, pcc.Storage, pcc.CPUCooler, 
                pcc.Case, pcc.PowerSupplyUnit, pcc.Socket,
                pcc.FormFactor, pcc.MemoryType, pcc.MotherboardInterface,
                pcc.Interface, pcc.CPUCoolerSocket, pcc.CaseFormFactor)
class ItemAdmin(admin.ModelAdmin):
    pass
