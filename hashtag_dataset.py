"""
hashtag_dataset.py — Curated Trending Hashtag Dataset
=====================================================
A static, categorised collection of trending hashtags across
five verticals. Used by the Hashtag Engine in content_modules.py
to blend AI-generated tags with real-world trending ones.
"""

# ---------------------------------------------------------------------------
# Trending hashtag pools (curated & periodically updatable)
# ---------------------------------------------------------------------------

TRENDING_HASHTAGS: dict[str, list[str]] = {
    "Fashion": [
        "#OOTD", "#FashionInspo", "#StreetStyle", "#StyleGuide",
        "#FashionTrends", "#WardrobeEssentials", "#SustainableFashion",
        "#LuxuryFashion", "#FashionBlogger", "#TrendAlert",
        "#FashionWeek", "#MinimalStyle", "#HighFashion",
        "#FashionDaily", "#OutfitIdeas", "#VintageStyle",
        "#DesignerWear", "#FashionLover", "#ChicStyle", "#RunwayReady",
    ],
    "Food": [
        "#Foodie", "#FoodPhotography", "#InstaFood", "#FoodBlogger",
        "#HealthyEating", "#HomeCooking", "#FoodLovers", "#Yummy",
        "#ChefLife", "#FoodGasm", "#CleanEating", "#Delicious",
        "#FoodStyling", "#RecipeOfTheDay", "#FarmToTable",
        "#GourmetFood", "#Brunch", "#FoodArt", "#MealPrep", "#Vegan",
    ],
    "Technology": [
        "#TechNews", "#AI", "#MachineLearning", "#StartupLife",
        "#Innovation", "#CyberSecurity", "#WebDev", "#Programming",
        "#TechTrends", "#DigitalTransformation", "#CloudComputing",
        "#DataScience", "#Blockchain", "#IoT", "#FutureTech",
        "#SaaS", "#DeepLearning", "#DevCommunity", "#OpenSource",
        "#TechStartup",
    ],
    "Lifestyle": [
        "#Lifestyle", "#SelfCare", "#Mindfulness", "#LifeGoals",
        "#DailyRoutine", "#Wellness", "#HealthyLifestyle", "#Motivation",
        "#GoodVibes", "#LifeHacks", "#PersonalGrowth", "#Positivity",
        "#MorningRoutine", "#WorkLifeBalance", "#TravelLifestyle",
        "#MinimalLiving", "#Aesthetic", "#SlowLiving", "#Grateful",
        "#LiveYourBestLife",
    ],
    "Business": [
        "#Entrepreneur", "#BusinessGrowth", "#StartUp", "#Leadership",
        "#Marketing", "#DigitalMarketing", "#BrandStrategy",
        "#ContentMarketing", "#SmallBusiness", "#Hustle",
        "#BusinessMindset", "#GrowthHacking", "#Networking",
        "#CEOLife", "#B2B", "#SalesStrategy", "#PersonalBranding",
        "#EcommerceTips", "#ScaleUp", "#BusinessTips",
    ],
}


def get_trending_hashtags(category: str, count: int = 10) -> list[str]:
    """
    Return up to *count* trending hashtags for the given category.

    Parameters
    ----------
    category : str
        One of: Fashion, Food, Technology, Lifestyle, Business.
        Case-insensitive matching is applied.
    count : int
        Maximum number of hashtags to return.

    Returns
    -------
    list[str]
        Hashtags list, or an empty list if the category is unknown.
    """
    # Case-insensitive lookup
    for key, tags in TRENDING_HASHTAGS.items():
        if key.lower() == category.strip().lower():
            return tags[:count]
    return []


def get_all_categories() -> list[str]:
    """Return the list of available hashtag categories."""
    return list(TRENDING_HASHTAGS.keys())
