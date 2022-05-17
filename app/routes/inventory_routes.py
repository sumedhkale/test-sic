from app import app

# Blueprint Configuration
inventory_bp = Blueprint(
    'inventory_bp', __name__,
    template_folder='templates',
    # static_folder='static',
    url_prefix='/inventory'
)


@inventory_bp.route('/')
def index():
    return "In inventory bp "
