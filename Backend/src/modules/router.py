from fastapi import APIRouter
from src.modules.auth.router.Login import router as login_router
from src.modules.auth.router.Register import router as register_router
from src.modules.auth.router.Logout import router as logout_router
from src.modules.typeLocation.router.TypeLocationRouter import router as type_location_router
from src.modules.typeMaterials.router.TypeMaterialRouter import router as type_material_router
from src.modules.materials.router.MaterialRouter import router as material_router
from src.modules.materials.router.LocationStockRouter import router as location_stock_router
from src.modules.companies.router.Company import router as company_router
from src.modules.locationsCompany.router.LocationCompany import router as location_company_router
from src.modules.orders.router.OrderRouter import router as order_router


router = APIRouter()

router.include_router(login_router)
router.include_router(register_router)
router.include_router(logout_router)
router.include_router(company_router)
router.include_router(location_company_router)
router.include_router(type_location_router)
router.include_router(type_material_router)
router.include_router(material_router)
router.include_router(location_stock_router)
router.include_router(order_router)