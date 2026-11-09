import asyncpg
from typing import List, Dict, Any, Optional

DATABASE_URL = "postgresql://jack@localhost/fapi"

async def geocode_address(city: str, street: Optional[str] = None, housenumber: Optional[str] = None) -> List[Dict[str, Any]]:
    """Поиск координат по адресу в БД (async версия)"""
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        if street and housenumber:
            rows = await conn.fetch("""
                SELECT 
                    address_full,
                    street,
                    housenumber, 
                    city,
                    ST_X(centroid) as longitude,
                    ST_Y(centroid) as latitude
                FROM buildings 
                WHERE city ILIKE $1 
                  AND street ILIKE $2 
                  AND housenumber = $3
            """, f'%{city}%', f'%{street}%', housenumber)
        
        elif street:
            rows = await conn.fetch("""
                SELECT 
                    address_full,
                    street,
                    housenumber,
                    city,
                    ST_X(centroid) as longitude,
                    ST_Y(centroid) as latitude
                FROM buildings 
                WHERE city ILIKE $1 
                  AND street ILIKE $2
                ORDER BY housenumber
                LIMIT 10
            """, f'%{city}%', f'%{street}%')
        
        else:
            rows = await conn.fetch("""
                SELECT 
                    address_full,
                    street,
                    housenumber,
                    city,
                    ST_X(centroid) as longitude,
                    ST_Y(centroid) as latitude
                FROM buildings 
                WHERE city ILIKE $1
                LIMIT 10
            """, f'%{city}%')
        
        return [
            {
                'address_full': row['address_full'],
                'street': row['street'],
                'housenumber': row['housenumber'],
                'city': row['city'],
                'longitude': float(row['longitude']),
                'latitude': float(row['latitude'])
            }
            for row in rows
        ]
        
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        await conn.close()