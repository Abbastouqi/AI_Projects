from sqlalchemy.orm import Session
from models.database import Laptop, SessionLocal, init_db
from datetime import datetime

def get_sample_laptops():
    """Sample Pakistani laptop data with realistic PKR prices (2024)"""
    return [
        # Budget FSC Student Laptops (60k-90k PKR)
        {
            "brand": "HP",
            "model": "15s-fq5007tu",
            "cpu": "Intel Core i3-1215U (6 cores, up to 4.4GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel UHD Graphics",
            "display_size": 15.6,
            "price_pkr": 85000,
            "battery_hours": 6.5,
            "weight_kg": 1.69,
            "ideal_for": ["FSC Student", "Office Work", "Basic Computing"],
            "source_url": "https://www.daraz.pk/products/hp-15s-fq5007tu"
        },
        {
            "brand": "Lenovo",
            "model": "V15 G3",
            "cpu": "AMD Ryzen 3 5300U (4 cores, up to 3.8GHz)",
            "ram_gb": 8,
            "storage_gb": 256,
            "storage_type": "SSD",
            "gpu": "AMD Radeon Graphics",
            "display_size": 15.6,
            "price_pkr": 72000,
            "battery_hours": 5.5,
            "weight_kg": 1.7,
            "ideal_for": ["FSC Student", "Basic Computing", "Document Work"],
            "source_url": "https://www.daraz.pk/products/lenovo-v15-g3"
        },
        {
            "brand": "Dell",
            "model": "Inspiron 15 3520",
            "cpu": "Intel Core i3-1215U (6 cores, up to 4.4GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel UHD Graphics",
            "display_size": 15.6,
            "price_pkr": 89000,
            "battery_hours": 7.0,
            "weight_kg": 1.65,
            "ideal_for": ["FSC Student", "Office Work", "Online Classes"],
            "source_url": "https://www.daraz.pk/products/dell-inspiron-15-3520"
        },
        
        # Mid-Range Programming Laptops (100k-140k PKR)
        {
            "brand": "HP",
            "model": "15s-fq5327tu",
            "cpu": "Intel Core i5-1235U (10 cores, up to 4.4GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 115000,
            "battery_hours": 7.5,
            "weight_kg": 1.69,
            "ideal_for": ["Programming", "Web Development", "CS Student"],
            "source_url": "https://www.daraz.pk/products/hp-15s-fq5327tu"
        },
        {
            "brand": "Lenovo",
            "model": "IdeaPad 3 15IAU7",
            "cpu": "Intel Core i5-1235U (10 cores, up to 4.4GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 108000,
            "battery_hours": 8.0,
            "weight_kg": 1.63,
            "ideal_for": ["Programming", "Software Development", "CS Student"],
            "source_url": "https://www.daraz.pk/products/lenovo-ideapad-3"
        },
        {
            "brand": "Dell",
            "model": "Inspiron 15 3530",
            "cpu": "Intel Core i5-1335U (10 cores, up to 4.6GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 125000,
            "battery_hours": 7.0,
            "weight_kg": 1.65,
            "ideal_for": ["Programming", "Data Science", "CS Student"],
            "source_url": "https://www.daraz.pk/products/dell-inspiron-15-3530"
        },
        {
            "brand": "ASUS",
            "model": "VivoBook 15 X1502ZA",
            "cpu": "Intel Core i5-1235U (10 cores, up to 4.4GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 112000,
            "battery_hours": 6.5,
            "weight_kg": 1.7,
            "ideal_for": ["Programming", "Graphic Design", "CS Student"],
            "source_url": "https://www.daraz.pk/products/asus-vivobook-15"
        },
        
        # High-End Programming/Engineering (140k-200k PKR)
        {
            "brand": "HP",
            "model": "Pavilion 15-eg2063TX",
            "cpu": "Intel Core i7-1255U (10 cores, up to 4.7GHz)",
            "ram_gb": 16,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "NVIDIA GeForce MX550 2GB",
            "display_size": 15.6,
            "price_pkr": 175000,
            "battery_hours": 8.0,
            "weight_kg": 1.75,
            "ideal_for": ["Programming", "Machine Learning", "Engineering", "Video Editing"],
            "source_url": "https://www.daraz.pk/products/hp-pavilion-15"
        },
        {
            "brand": "Lenovo",
            "model": "IdeaPad Slim 5 16IAH8",
            "cpu": "Intel Core i7-12650H (10 cores, up to 4.7GHz)",
            "ram_gb": 16,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 16.0,
            "price_pkr": 165000,
            "battery_hours": 9.0,
            "weight_kg": 1.89,
            "ideal_for": ["Programming", "Data Science", "Engineering", "CS Student"],
            "source_url": "https://www.daraz.pk/products/lenovo-ideapad-slim-5"
        },
        {
            "brand": "Dell",
            "model": "Inspiron 15 5530",
            "cpu": "Intel Core i7-1355U (10 cores, up to 5.0GHz)",
            "ram_gb": 16,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 185000,
            "battery_hours": 8.5,
            "weight_kg": 1.66,
            "ideal_for": ["Programming", "Machine Learning", "Engineering", "Data Science"],
            "source_url": "https://www.daraz.pk/products/dell-inspiron-15-5530"
        },
        
        # Budget AMD Options (75k-95k PKR)
        {
            "brand": "Lenovo",
            "model": "V15 G3 Ryzen 5",
            "cpu": "AMD Ryzen 5 5500U (6 cores, up to 4.0GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "AMD Radeon Graphics",
            "display_size": 15.6,
            "price_pkr": 92000,
            "battery_hours": 6.0,
            "weight_kg": 1.7,
            "ideal_for": ["FSC Student", "Programming", "Office Work"],
            "source_url": "https://www.daraz.pk/products/lenovo-v15-ryzen5"
        },
        {
            "brand": "ASUS",
            "model": "VivoBook 15 M1502YA",
            "cpu": "AMD Ryzen 5 7520U (4 cores, up to 4.3GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "AMD Radeon 610M",
            "display_size": 15.6,
            "price_pkr": 95000,
            "battery_hours": 7.0,
            "weight_kg": 1.7,
            "ideal_for": ["FSC Student", "Programming", "Multimedia"],
            "source_url": "https://www.daraz.pk/products/asus-vivobook-m1502ya"
        },
        {
            "brand": "HP",
            "model": "15s-eq2144AU",
            "cpu": "AMD Ryzen 5 5500U (6 cores, up to 4.0GHz)",
            "ram_gb": 8,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "AMD Radeon Graphics",
            "display_size": 15.6,
            "price_pkr": 88000,
            "battery_hours": 6.5,
            "weight_kg": 1.69,
            "ideal_for": ["FSC Student", "Office Work", "Basic Programming"],
            "source_url": "https://www.daraz.pk/products/hp-15s-eq2144au"
        },
        
        # Premium Options (200k+ PKR)
        {
            "brand": "HP",
            "model": "Envy x360 15-fh0033dx",
            "cpu": "AMD Ryzen 7 7730U (8 cores, up to 4.5GHz)",
            "ram_gb": 16,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "AMD Radeon Graphics",
            "display_size": 15.6,
            "price_pkr": 215000,
            "battery_hours": 10.0,
            "weight_kg": 1.74,
            "ideal_for": ["Programming", "Engineering", "Machine Learning", "Content Creation"],
            "source_url": "https://www.daraz.pk/products/hp-envy-x360"
        },
        {
            "brand": "Dell",
            "model": "Inspiron 16 5630",
            "cpu": "Intel Core i7-1360P (12 cores, up to 5.0GHz)",
            "ram_gb": 16,
            "storage_gb": 1024,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 16.0,
            "price_pkr": 225000,
            "battery_hours": 9.5,
            "weight_kg": 1.87,
            "ideal_for": ["Programming", "Engineering", "Data Science", "Video Editing"],
            "source_url": "https://www.daraz.pk/products/dell-inspiron-16-5630"
        },
        {
            "brand": "Lenovo",
            "model": "ThinkBook 15 G4",
            "cpu": "Intel Core i7-1255U (10 cores, up to 4.7GHz)",
            "ram_gb": 16,
            "storage_gb": 512,
            "storage_type": "SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display_size": 15.6,
            "price_pkr": 195000,
            "battery_hours": 11.0,
            "weight_kg": 1.7,
            "ideal_for": ["Programming", "Business", "Engineering", "Professional Work"],
            "source_url": "https://www.daraz.pk/products/lenovo-thinkbook-15"
        }
    ]

def seed_database():
    """Initialize database with sample laptop data"""
    # Create tables
    init_db()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Laptop).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} laptops. Skipping seed.")
            return
        
        # Add sample laptops
        laptops_data = get_sample_laptops()
        for laptop_data in laptops_data:
            laptop = Laptop(**laptop_data)
            db.add(laptop)
        
        db.commit()
        print(f"Successfully seeded database with {len(laptops_data)} laptops!")
        
        # Print summary
        print("\n=== Database Summary ===")
        print(f"Total Laptops: {db.query(Laptop).count()}")
        print(f"HP Laptops: {db.query(Laptop).filter(Laptop.brand == 'HP').count()}")
        print(f"Dell Laptops: {db.query(Laptop).filter(Laptop.brand == 'Dell').count()}")
        print(f"Lenovo Laptops: {db.query(Laptop).filter(Laptop.brand == 'Lenovo').count()}")
        print(f"ASUS Laptops: {db.query(Laptop).filter(Laptop.brand == 'ASUS').count()}")
        print(f"\nPrice Range: PKR {db.query(Laptop).order_by(Laptop.price_pkr).first().price_pkr:,} - PKR {db.query(Laptop).order_by(Laptop.price_pkr.desc()).first().price_pkr:,}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
