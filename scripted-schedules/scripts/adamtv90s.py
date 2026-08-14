#!/usr/bin/python3

from datetime import timedelta

from etv_client.models.content_smart_collection import ContentSmartCollection
from etv_client.models.content_collection import ContentCollection
from etv_client.models.playout_count import PlayoutCount
from etv_client.models.playout_pad_until_exact import PlayoutPadUntilExact
from etv_client.models.control_wait_until_exact import ControlWaitUntilExact
from etv_client.models.control_watermark_on import ControlWatermarkOn
from etv_client.models.control_watermark_off import ControlWatermarkOff
from etv_client.models.control_graphics_on import ControlGraphicsOn
from etv_client.models.control_graphics_off import ControlGraphicsOff
from etv_client.models.control_start_epg_group import ControlStartEpgGroup


# ---------------------------------------------------------
# WATERMARKS
# ---------------------------------------------------------

NORMAL_WATERMARK = "AdaMTV 90s Colour Logo"
HOUSE_WATERMARK = "AdaMTV 90's Colour House Classics Logo"
BRITPOP_WATERMARK = "AdaMTV 90's Colour Britpop Logo"
WATERMARK_1995 = "AdaMTV 90's Colour 1995 Logo"
WATERMARK_1996 = "AdaMTV 90's Colour 1996 Logo"


# ---------------------------------------------------------
# FEATURED ARTIST GRAPHICS
# ---------------------------------------------------------

BLUR_GRAPHIC = "text/featured-artist-blur.yml"
OASIS_GRAPHIC = "text/featured-artist-oasis.yml"

# ---------------------------------------------------------
# CUE DOT
# ---------------------------------------------------------

CUE_DOT_GRAPHIC = "motion/cue-dot.yml"

# ---------------------------------------------------------
# CONTENT
# ---------------------------------------------------------

def define_content(api, context, build_id):

    # Main rotation
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="MAIN",
            smartCollection="All Music Videos",
            order="shuffle"
        )
    )

    # House Classics
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="HOUSE",
            smartCollection="House Classics",
            order="shuffle"
        )
    )

    # Britpop
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="BRITPOP",
            smartCollection="Britpop",
            order="shuffle"
        )
    )

    # Blur
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="BLUR",
            smartCollection="Blur",
            order="shuffle"
        )
    )

    # Oasis
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="OASIS",
            smartCollection="Oasis",
            order="shuffle"
        )
    )

    # 1995 Music Videos
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="SPECIAL1995",
            smartCollection="1995 Music Videos",
            order="shuffle"
        )
    )

    # 1996 Music Videos
    api.add_smart_collection(
        build_id,
        ContentSmartCollection(
            key="SPECIAL1996",
            smartCollection="1996 Music Videos",
            order="shuffle"
        )
    )

    # Manual collections
    api.add_collection(
        build_id,
        ContentCollection(
            key="BRB",
            collection="We'll Be Right Back",
            order="shuffle"
        )
    )

    api.add_collection(
        build_id,
        ContentCollection(
            key="ADS",
            collection="All Commercials",
            order="shuffle"
        )
    )

    api.add_collection(
        build_id,
        ContentCollection(
            key="BACK",
            collection="We Are Back",
            order="shuffle"
        )
    )


def reset_playout(api, context, build_id):
    return context


# ---------------------------------------------------------
# STANDARD CYCLE
# ---------------------------------------------------------

def add_cycle(api, context, build_id, content, story=False):

    # -----------------------------------------------------
    # MUSIC VIDEO 1
    # -----------------------------------------------------

    turn_graphic_on(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    turn_graphic_on(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_on(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_on(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    context = api.add_count(
        build_id,
        PlayoutCount(
            content=content,
            count=1
        )
    )

    turn_graphic_off(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    turn_graphic_off(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_off(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_off(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    # -----------------------------------------------------
    # MUSIC VIDEO 2
    # -----------------------------------------------------

    turn_graphic_on(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    turn_graphic_on(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_on(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_on(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    context = api.add_count(
        build_id,
        PlayoutCount(
            content=content,
            count=1
        )
    )

    turn_graphic_off(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    turn_graphic_off(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_off(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_off(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    # -----------------------------------------------------
    # MUSIC VIDEO 3
    # -----------------------------------------------------

    # Turn on the ITV-style cue dot
    turn_graphic_on(
        api,
        build_id,
        CUE_DOT_GRAPHIC
    )

    # Animated Now Playing framework
    turn_graphic_on(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    # Dynamic artist/title metadata
    turn_graphic_on(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_on(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_on(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    # Third music video
    # The cue dot itself starts 10 seconds before
    # this video's end, according to the motion graphic YAML.
    context = api.add_count(
        build_id,
        PlayoutCount(
            content=content,
            count=1
        )
    )

    # Turn the cue dot off before the break material
    turn_graphic_off(
        api,
        build_id,
        CUE_DOT_GRAPHIC
    )

    turn_graphic_off(
        api,
        build_id,
        "motion/adamtv-now-playing-final.yml"
    )

    turn_graphic_off(
        api,
        build_id,
        "text/adamtv-now-playing.yml"
    )

    turn_graphic_off(
    	api,
    	build_id,
    	"text/adamtv-now-playing-end.yml"
    )

    if story:
        turn_graphic_off(
            api,
            build_id,
            "text/story-behind-the-song.yml"
        )

    # Break
    context = api.add_count(
        build_id,
        PlayoutCount(
            content="BRB",
            count=1
        )
    )

    context = api.add_count(
        build_id,
        PlayoutCount(
            content="ADS",
            count=2
        )
    )

    context = api.add_count(
        build_id,
        PlayoutCount(
            content="BACK",
            count=1
        )
    )

    return context

# ---------------------------------------------------------
# WEEKLY SPECIALS
#
# weekday:
# Monday = 0
# Tuesday = 1
# Wednesday = 2
# Thursday = 3
# Friday = 4
# Saturday = 5
# Sunday = 6
# ---------------------------------------------------------

def get_week_start(now):

    return (
        now
        - timedelta(days=now.weekday())
    ).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )


def get_weekly_events(now):

    week = get_week_start(now)

    events = [

        # Monday 12:00-14:00
        (
            week + timedelta(days=0, hours=12),
            week + timedelta(days=0, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True
        ),

        # Tuesday 12:00-14:00
        (
            week + timedelta(days=1, hours=12),
            week + timedelta(days=1, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True
        ),

        # Wednesday 12:00-14:00
        (
            week + timedelta(days=2, hours=12),
            week + timedelta(days=2, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True
        ),

        # Thursday 12:00-14:00
        (
            week + timedelta(days=3, hours=12),
            week + timedelta(days=3, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True
        ),

        # Friday 12:00-14:00
        (
            week + timedelta(days=4, hours=12),
            week + timedelta(days=4, hours=14),
            "The Story Behind the Song",
            "MAIN",
            NORMAL_WATERMARK,
            None,
            True
        ),

        # Tuesday 19:00-20:00
        (
            week + timedelta(days=1, hours=19),
            week + timedelta(days=1, hours=20),
            "Feature Hour: 1996",
            "SPECIAL1996",
            WATERMARK_1996,
            None,
	    False
        ),

        # Wednesday 19:00-20:00
        (
            week + timedelta(days=2, hours=19),
            week + timedelta(days=2, hours=20),
            "Feature Hour: 1995",
            "SPECIAL1995",
            WATERMARK_1995,
            None,
	    False
        ),

        # Friday 19:00-21:00
        (
            week + timedelta(days=4, hours=19),
            week + timedelta(days=4, hours=21),
            "House Classics",
            "HOUSE",
            HOUSE_WATERMARK,
            None,
	    False
        ),

        # Saturday 08:00 - Saturday 23:00
        (
	    week + timedelta(days=5, hours=8),
    	    week + timedelta(days=5, hours=23),
            "Britpop",
            "BRITPOP",
            BRITPOP_WATERMARK,
            None,
	    False
        ),

        # Sunday 15:00-16:00
        (
            week + timedelta(days=6, hours=15),
            week + timedelta(days=6, hours=16),
            "Featured Artist: Blur",
            "BLUR",
            NORMAL_WATERMARK,
            BLUR_GRAPHIC,
	    False
        ),

        # Sunday 16:00-17:00
        (
            week + timedelta(days=6, hours=16),
            week + timedelta(days=6, hours=17),
            "Featured Artist: Oasis",
            "OASIS",
            NORMAL_WATERMARK,
            OASIS_GRAPHIC,
	    False
        )
    ]

    return events


def find_next_special(now):

    events = get_weekly_events(now)

    # If we're currently inside a special, return it.
    for event in events:

        start, end, name, content, watermark, graphic, story = event

        if start <= now < end:
            return event

    # Otherwise find the next event.
    future_events = [
        event
        for event in events
        if event[0] > now
    ]

    if future_events:
        return future_events[0]

    # We've passed all this week's events.
    # Build next week's events.
    next_week = now + timedelta(days=7)

    return get_weekly_events(next_week)[0]


# ---------------------------------------------------------
# WATERMARK / GRAPHICS / EPG
# ---------------------------------------------------------

def set_watermark(api, build_id, watermark):

    api.watermark_off(
        build_id,
        ControlWatermarkOff()
    )

    api.watermark_on(
        build_id,
        ControlWatermarkOn(
            watermark=[watermark]
        )
    )


def turn_graphic_on(api, build_id, graphic):

    if graphic:

        api.graphics_on(
            build_id,
            ControlGraphicsOn(
                graphics=[graphic]
            )
        )


def turn_graphic_off(api, build_id, graphic):

    if graphic:

        api.graphics_off(
            build_id,
            ControlGraphicsOff(
                graphics=[graphic]
            )
        )


def start_epg_group(api, build_id, title):

    api.start_epg_group(
        build_id,
        ControlStartEpgGroup(
            advance=True,
            customTitle=title
        )
    )


def stop_epg_group(api, build_id):

    api.stop_epg_group(build_id)


# ---------------------------------------------------------
# BUILD A SPECIAL
# ---------------------------------------------------------

def build_special(
    api,
    context,
    build_id,
    start,
    end,
    name,
    content,
    watermark,
    graphic,
    story
):

    # Start EPG programme
    start_epg_group(
        api,
        build_id,
        name
    )

    # Switch watermark
    set_watermark(
        api,
        build_id,
        watermark
    )

    # Turn on featured artist graphic if required
    turn_graphic_on(
        api,
        build_id,
        graphic
    )

    # Fill the special with normal cycles
    while (
        not context.is_done
        and context.current_time < end
    ):

        previous_time = context.current_time

        context = add_cycle(
            api,
            context,
            build_id,
            content,
	    story=story
        )

        # Cycle crossed the end boundary
        if context.current_time > end:

            context = api.pad_until_exact(
                build_id,
                PlayoutPadUntilExact(
                    content=content,
                    when=end,
                    trim=True,
                    stopBeforeEnd=True
                )
            )

            break

        # Safety
        if context.current_time <= previous_time:
            break

    # Turn off featured graphic
    turn_graphic_off(
        api,
        build_id,
        graphic
    )

    # Return to normal watermark
    set_watermark(
        api,
        build_id,
        NORMAL_WATERMARK
    )

    # Finish EPG programme
    stop_epg_group(
        api,
        build_id
    )

    return context


# ---------------------------------------------------------
# MAIN PLAYOUT BUILDER
# ---------------------------------------------------------

def build_playout(api, context, build_id):

    while not context.is_done:

        now = context.current_time

        (
            special_start,
            special_end,
            special_name,
            special_content,
            special_watermark,
            special_graphic,
	    special_story
        ) = find_next_special(now)

        # -------------------------------------------------
        # NORMAL PROGRAMMING BEFORE NEXT SPECIAL
        # -------------------------------------------------

        if now < special_start:

            # Start normal EPG programme
            start_epg_group(
                api,
                build_id,
                "Non-stop 90s"
            )

            while (
                not context.is_done
                and context.current_time < special_start
            ):

                previous_time = context.current_time

                context = add_cycle(
                    api,
                    context,
                    build_id,
                    "MAIN"
                )

                # Cycle crossed the special boundary
                if context.current_time > special_start:

                    context = api.pad_until_exact(
                        build_id,
                        PlayoutPadUntilExact(
                            content="MAIN",
                            when=special_start,
                            trim=True,
                            stopBeforeEnd=True
                        )
                    )

                    break

                # Safety
                if context.current_time <= previous_time:
                    break

            # Finish normal EPG programme
            stop_epg_group(
                api,
                build_id
            )

            if context.is_done:
                break

            # If there is still a gap, wait exactly until
            # the special begins.
            if context.current_time < special_start:

                context = api.wait_until_exact(
                    build_id,
                    ControlWaitUntilExact(
                        when=special_start,
                        rewindOnReset=False
                    )
                )

        if context.is_done:
            break

        # -------------------------------------------------
        # SPECIAL
        # -------------------------------------------------

        context = build_special(
            api,
            context,
            build_id,
            special_start,
            special_end,
            special_name,
            special_content,
            special_watermark,
            special_graphic,
	    special_story
        )

    return context
