"""
Crop agricultural knowledge base for the 22 supported crop varieties in the dataset.
Provides verified agronomic characteristics: general description, growing season,
soil requirements, and water requirements.
"""

CROP_DETAILS = {
    'apple': {
        'name': 'Apple',
        'emoji': '🍎',
        'category': 'Temperate Fruit',
        'description': 'A temperate orchard fruit crop that requires adequate winter chilling hours and mild summer temperatures for optimal fruit set and sugar accumulation.',
        'season': 'Perennial (Autumn harvest; planted in late winter/early spring)',
        'soil': 'Deep, fertile, well-drained loamy soil rich in organic matter (pH 5.5 - 6.8).',
        'water_requirement': 'Moderate to High (100 - 150 mm regular precipitation or scheduled orchard drip irrigation).'
    },
    'banana': {
        'name': 'Banana',
        'emoji': '🍌',
        'category': 'Tropical Fruit',
        'description': 'A fast-growing, heavy-feeding tropical herbaceous plant requiring consistent warmth, moisture, and high nutrient replenishment for bountiful bunches.',
        'season': 'Year-round planting in tropical and frost-free subtropical climates.',
        'soil': 'Deep, rich, well-drained alluvial or loamy soil with high organic content (pH 6.0 - 7.5).',
        'water_requirement': 'High (150 - 250 mm monthly water requirement; sensitive to drought stress).'
    },
    'blackgram': {
        'name': 'Blackgram (Urad)',
        'emoji': '🥣',
        'category': 'Pulse / Legume',
        'description': 'A nutritious warm-season legume crop valued for dietary protein, soil enrichment via biological nitrogen fixation, and green manuring.',
        'season': 'Kharif (Monsoon) and Summer crop.',
        'soil': 'Loamy to clay-loam soils with good drainage and moderate moisture retention (pH 6.0 - 7.5).',
        'water_requirement': 'Moderate (50 - 80 mm; sensitive to waterlogging during flowering).'
    },
    'chickpea': {
        'name': 'Chickpea (Gram)',
        'emoji': '🧆',
        'category': 'Pulse / Legume',
        'description': 'A cool-season protein-rich pulse crop that naturally fixes atmospheric nitrogen into the soil, requiring mild temperatures and dry ripening weather.',
        'season': 'Rabi (Winter season; October - April).',
        'soil': 'Deep black cotton soils, alluvial soils, or well-drained sandy loam (pH 6.0 - 8.0).',
        'water_requirement': 'Low to Moderate (35 - 65 mm; drought-tolerant and sensitive to excessive moisture).'
    },
    'coconut': {
        'name': 'Coconut',
        'emoji': '🥥',
        'category': 'Plantation Crop',
        'description': 'A tall perennial coastal palm providing tender water, copra, oil, and coir. Flourishes under humid tropical maritime climates.',
        'season': 'Perennial (Year-round production after reaching maturity).',
        'soil': 'Coastal sands, alluvial floodplains, and red sandy loams with excellent drainage (pH 5.2 - 8.0).',
        'water_requirement': 'High (150 - 250 mm regular rainfall or steady subsoil water supply).'
    },
    'coffee': {
        'name': 'Coffee (Arabica / Robusta)',
        'emoji': '☕',
        'category': 'Plantation Crop',
        'description': 'A high-elevation tropical shade-grown plantation crop cultivated for aromatic beans. Thrives in cool, mist-covered mountain slopes.',
        'season': 'Perennial (Flowering triggered by spring rains, winter harvest).',
        'soil': 'Porous, deep, volcanic or forest loam rich in humus and organic matter (pH 5.5 - 6.5).',
        'water_requirement': 'Moderate to High (150 - 200 mm well-distributed annual rainfall with a dry ripening period).'
    },
    'cotton': {
        'name': 'Cotton',
        'emoji': '☁️',
        'category': 'Commercial Fiber',
        'description': 'A major cash crop providing natural textile fibers. Requires warm growing temperatures, ample sunshine, and a dry picking season.',
        'season': 'Kharif (Sown April - June, harvested October - February).',
        'soil': 'Deep black clayey soils (Regur) or fertile alluvial loams with good aeration (pH 6.0 - 8.0).',
        'water_requirement': 'Moderate (60 - 110 mm rainfall; needs warm, rain-free weather during boll opening).'
    },
    'grapes': {
        'name': 'Grapes',
        'emoji': '🍇',
        'category': 'Subtropical / Temperate Fruit',
        'description': 'A deciduous perennial woody vine cultivated for fresh table fruit, raisins, and juice. Prefers hot dry summers and mild winters.',
        'season': 'Perennial (Spring and early summer harvest depending on pruning schedule).',
        'soil': 'Well-drained sandy-loam, gravelly, or alluvial soils with permeable subsoil (pH 6.5 - 8.5).',
        'water_requirement': 'Moderate (50 - 90 mm; low humidity during ripening minimizes fungal leaf infections).'
    },
    'jute': {
        'name': 'Jute',
        'emoji': '🌾',
        'category': 'Commercial Fiber',
        'description': 'Known as the "golden fiber", jute is a fast-growing commercial bast fiber crop thriving in warm, tropical, high-rainfall delta floodplains.',
        'season': 'Kharif (Sown March - May, harvested July - September).',
        'soil': 'Rich riverine alluvial silt and clay loam regularly replenished by monsoon deposits (pH 6.0 - 7.5).',
        'water_requirement': 'High (150 - 250 mm rainfall accompanied by high relative humidity).'
    },
    'kidneybeans': {
        'name': 'Kidney Beans (Rajma)',
        'emoji': '🫘',
        'category': 'Pulse / Legume',
        'description': 'A protein-dense legume cultivated extensively in temperate valley highlands and cool plains during frost-free periods.',
        'season': 'Kharif in hilly tracts; Late Kharif / Spring in plains.',
        'soil': 'Deep, light, fertile, well-aerated loamy soil free from soil compaction (pH 5.8 - 6.8).',
        'water_requirement': 'Moderate (60 - 100 mm evenly distributed; intolerant to water stagnation).'
    },
    'lentil': {
        'name': 'Lentil (Masoor)',
        'emoji': '🍲',
        'category': 'Pulse / Legume',
        'description': 'An ancient cool-season pulse crop celebrated for rich nutritional value, rapid cooking time, and hardy performance in rainfed dry farming.',
        'season': 'Rabi (Winter season; October - November sowing).',
        'soil': 'Alluvial loams and clay loams with neutral to slightly alkaline reaction (pH 6.0 - 7.5).',
        'water_requirement': 'Low to Moderate (35 - 65 mm; requires dry weather during pod maturation).'
    },
    'maize': {
        'name': 'Maize (Corn)',
        'emoji': '🌽',
        'category': 'Cereal Grain',
        'description': 'A versatile high-yielding cereal grain serving as human food, animal feed, and industrial starch. Grows well in diverse agro-ecological zones.',
        'season': 'Kharif (Monsoon), Rabi (Winter), and Spring.',
        'soil': 'Well-drained, fertile sandy-loam to silty-loam soils with high organic matter (pH 5.8 - 7.5).',
        'water_requirement': 'Moderate (60 - 110 mm rainfall; critical moisture needed during tasseling and silking).'
    },
    'mango': {
        'name': 'Mango',
        'emoji': '🥭',
        'category': 'Tropical Fruit',
        'description': 'The "King of Fruits", a deep-rooted evergreen tropical orchard tree that flourishes in tropical and subtropical climates with a distinct dry period for flowering.',
        'season': 'Perennial (Flowering in winter, harvesting from April to July).',
        'soil': 'Deep, well-drained alluvial, loamy or lateritic soils with good drainage (pH 5.5 - 7.5).',
        'water_requirement': 'Moderate (60 - 120 mm annual distribution; dry conditions during flowering are essential).'
    },
    'mothbeans': {
        'name': 'Moth Beans (Matki)',
        'emoji': '🌿',
        'category': 'Arid Pulse',
        'description': 'An exceptionally drought-resistant short-stature arid pulse crop that thrives in sandy soils and prevents erosion in dryland agroecosystems.',
        'season': 'Kharif (Monsoon season in arid/semi-arid regions).',
        'soil': 'Light sandy to sandy-loam soils with rapid drainage (pH 6.5 - 8.0).',
        'water_requirement': 'Very Low (30 - 55 mm; highly tolerant of heat and dry spells).'
    },
    'mungbean': {
        'name': 'Mungbean (Green Gram)',
        'emoji': '🌱',
        'category': 'Pulse / Legume',
        'description': 'A short-duration warm-season pulse crop ideally suited for crop rotation, intercropping, and quick income between major cropping seasons.',
        'season': 'Kharif, Spring, and Summer crop (matures in 60 - 75 days).',
        'soil': 'Well-drained loam to sandy-loam soils (pH 6.2 - 7.5).',
        'water_requirement': 'Low to Moderate (40 - 70 mm; sensitive to waterlogging).'
    },
    'muskmelon': {
        'name': 'Muskmelon',
        'emoji': '🍈',
        'category': 'Cucurbit / Summer Fruit',
        'description': 'A trailing warm-season vine crop producing sweet, fragrant fruit. Requires warm dry weather and plenty of sunshine during ripening.',
        'season': 'Zaid (Summer season; sown February - March).',
        'soil': 'Sandy loam, alluvial riverbed soil with good warm aeration (pH 6.0 - 7.0).',
        'water_requirement': 'Moderate (50 - 85 mm; avoid wetting vines and fruit directly to protect quality).'
    },
    'orange': {
        'name': 'Orange (Citrus)',
        'emoji': '🍊',
        'category': 'Citrus Fruit',
        'description': 'A popular subtropical citrus fruit celebrated for vitamin C and juiciness. Requires warm sunny days, cool nights, and well-aerated root zones.',
        'season': 'Perennial (Winter and early spring fruit harvest).',
        'soil': 'Light to medium well-drained sandy loam or alluvial soil with deep water table (pH 6.0 - 7.5).',
        'water_requirement': 'Moderate (80 - 120 mm regular watering; extremely intolerant to stagnant water).'
    },
    'papaya': {
        'name': 'Papaya',
        'emoji': '🍈',
        'category': 'Tropical Fruit',
        'description': 'A fast-yielding herbaceous fruit plant that bears nutritious fruits year-round in frost-free tropical and subtropical areas.',
        'season': 'Year-round planting in tropical zones.',
        'soil': 'Light, rich, fertile sandy loam or alluvial soil with high drainage capacity (pH 6.0 - 7.0).',
        'water_requirement': 'Moderate to High (100 - 160 mm; zero tolerance for waterlogging which causes root rot).'
    },
    'pigeonpeas': {
        'name': 'Pigeon Peas (Arhar / Toor)',
        'emoji': '🪴',
        'category': 'Pulse / Legume',
        'description': 'A resilient, deep-rooting, long-duration pulse crop widely grown in rainfed drylands to supply staple dal and enrich deep soil horizons.',
        'season': 'Kharif (Sown with the onset of monsoon, harvested in winter).',
        'soil': 'Deep loamy to heavy black soils with effective drainage (pH 6.0 - 7.5).',
        'water_requirement': 'Low to Moderate (60 - 100 mm; excellent drought recovery due to deep taproot).'
    },
    'pomegranate': {
        'name': 'Pomegranate',
        'emoji': '🫐',
        'category': 'Subtropical Fruit',
        'description': 'A drought-tolerant high-value fruit crop suitable for semi-arid zones, valued for antioxidant-packed seeds and adaptable growing habits.',
        'season': 'Perennial (Regulated fruiting flushes: Ambe, Mrig, or Hasta bahar).',
        'soil': 'Deep, well-drained loamy to light alluvial soils (pH 6.5 - 8.0).',
        'water_requirement': 'Low to Moderate (50 - 85 mm; responds well to efficient drip irrigation).'
    },
    'rice': {
        'name': 'Rice (Paddy)',
        'emoji': '🌾',
        'category': 'Cereal Grain',
        'description': 'The world’s foremost staple food crop. Cultivated in flooded paddy fields requiring abundant warmth, standing water, and high seasonal rainfall.',
        'season': 'Kharif (Monsoon season; also Rabi/Boro in assured irrigation zones).',
        'soil': 'Heavy clayey or silty-loam soils with an impervious subsoil layer to retain standing water (pH 5.5 - 7.0).',
        'water_requirement': 'High (180 - 300 mm water depth; requires standing water during vegetative phases).'
    },
    'watermelon': {
        'name': 'Watermelon',
        'emoji': '🍉',
        'category': 'Cucurbit / Summer Fruit',
        'description': 'A refreshing summer vine fruit with sweet hydrating pulp. Thrives under long, warm, sunny days with dry atmospheric conditions.',
        'season': 'Zaid (Summer season; sown February - March).',
        'soil': 'Deep, warm, well-drained sandy loam or riverbed alluvial soils (pH 6.0 - 7.2).',
        'water_requirement': 'Moderate (45 - 75 mm; regular soil moisture during early growth, dry during fruit sweetening).'
    }
}


def get_crop_info(crop_label):
    """
    Safely retrieves crop agricultural information for any predicted label.
    Falls back to a clean default if an unmapped label is encountered.
    """
    key = str(crop_label).strip().lower()
    if key in CROP_DETAILS:
        return CROP_DETAILS[key]
    
    # Clean fallback for unexpected labels
    return {
        'name': key.capitalize(),
        'emoji': '🌱',
        'category': 'Agricultural Crop',
        'description': f'A viable agricultural crop recommended for your specific soil and climatic parameters.',
        'season': 'Seasonal (consult local agricultural extension services)',
        'soil': 'Fertile, well-drained agricultural soil.',
        'water_requirement': 'Moderate (adjust based on seasonal rainfall and soil moisture).'
    }
