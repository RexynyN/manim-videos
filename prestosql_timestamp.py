from manim import *

class PrestoTimestampUnderTheHood(Scene):
    def construct(self):
        # Defining consistent colors
        C_UTC = BLUE
        C_TZ = YELLOW
        C_PICO = GREEN
        C_PRIMITIVE = RED_D
        C_OBJECT = PURPLE_D

        # Introduction
        title = Title("PrestoSQL/Trino: Timestamps Under the Hood", font_size=40)
        self.play(Write(title))

        intro_text = Text("Core Principle: Normalization to UTC Epoch", font_size=24).to_edge(UP, buff=1.5)
        epoch_line = NumberLine(
            x_range=[1970, 2030, 10],
            length=10,
            include_numbers=True,
            label_direction=UP,
        ).move_to(DOWN * 0.5)
        epoch_label = Text("1970-01-01 (Epoch)", font_size=20, color=C_UTC).next_to(epoch_line.n2p(1970), DOWN)
        
        self.play(Write(intro_text), Create(epoch_line), Write(epoch_label))
        self.wait(2)
        self.play(FadeOut(intro_text), FadeOut(epoch_line), FadeOut(epoch_label))

        ########################################################################
        # Section 1: TIMESTAMP (No Time Zone)
        ########################################################################
        section_1_title = Text("Part 1: TIMESTAMP (No Time Zone)", font_size=32).to_edge(UP, buff=1.5)
        self.play(Write(section_1_title))

        # Subsection 1A: Short Timestamp (p <= 6)
        p_short_txt = Text("Precision p <= 6 (Microseconds)", font_size=28).next_to(section_1_title, DOWN)
        self.play(Write(p_short_txt))

        primitive_box = Rectangle(width=8, height=1.5, color=C_PRIMITIVE, fill_opacity=0.2)
        primitive_label = Text("64-bit long (primitive)", font_size=20, color=C_PRIMITIVE).next_to(primitive_box, UP)
        primitive_content = Text("Micros since Epoch\n(e.g., 1698246000000000)", font_size=24).move_to(primitive_box)

        self.play(Create(primitive_box), Write(primitive_label))
        self.play(Write(primitive_content))
        self.wait(2)

        # Transition to Long Timestamp
        self.play(
            FadeOut(primitive_box), FadeOut(primitive_label), FadeOut(primitive_content),
            FadeOut(p_short_txt)
        )

        # Subsection 1B: Long Timestamp (p > 6)
        p_long_txt = Text("Precision p > 6 (Nanoseconds/Picoseconds)", font_size=28).next_to(section_1_title, DOWN)
        self.play(Write(p_long_txt))

        long_ts_container = RoundedRectangle(width=9, height=2.5, corner_radius=0.2, color=C_OBJECT, fill_opacity=0.1)
        long_ts_label = Text("LongTimestamp (Java Object)", font_size=20, color=C_OBJECT).next_to(long_ts_container, UP)

        field_micros = VGroup(
            Rectangle(width=4, height=0.7, color=C_UTC),
            Text("epochMicros (long)", font_size=20)
        ).arrange(DOWN, center=False, buff=0.1)
        
        field_picos = VGroup(
            Rectangle(width=4, height=0.7, color=C_PICO),
            Text("picosOfMicro (int)", font_size=20)
        ).arrange(DOWN, center=False, buff=0.1)

        fields_group = VGroup(field_micros, field_picos).arrange(RIGHT, buff=0.5).move_to(long_ts_container)

        self.play(Create(long_ts_container), Write(long_ts_label))
        self.play(Create(field_micros), Create(field_picos))
        self.wait(2)

        self.play(FadeOut(long_ts_container), FadeOut(long_ts_label), FadeOut(fields_group), FadeOut(section_1_title), FadeOut(p_long_txt))


        ########################################################################
        # Section 2: TIMESTAMP WITH TIME ZONE
        ########################################################################
        section_2_title = Text("Part 2: TIMESTAMP WITH TIME ZONE", font_size=32).to_edge(UP, buff=1.5)
        self.play(Write(section_2_title))

        # The Challenge Concept
        tz_string = Text("'America/Sao_Paulo'", color=RED).shift(LEFT * 3)
        arrow_challenge = Arrow(start=tz_string.get_right(), end=RIGHT * 2)
        tz_key_concept = Text("TimeZoneKey (short ID: 450)", color=C_TZ).shift(RIGHT * 3)

        self.play(Write(tz_string))
        self.play(GrowArrow(arrow_challenge), TransformFromCopy(tz_string, tz_key_concept))
        self.wait(1)
        self.play(FadeOut(tz_string), FadeOut(arrow_challenge), FadeOut(tz_key_concept))


        # Subsection 2A: Bit Packing (The complex part)
        packing_title = Text("Precision p <= 3 (Millis): Bit Packing Strategy", font_size=28).next_to(section_2_title, DOWN)
        self.play(Write(packing_title))

        # The main 64-bit container
        full_long_bar = Rectangle(width=12, height=1.5, color=WHITE).shift(DOWN * 0.5)
        bar_label = Text("The Packed 64-bit long", font_size=20).next_to(full_long_bar, UP)
        self.play(Create(full_long_bar), Write(bar_label))

        # Splitting visually
        
        high_bits_rect = Rectangle(width=12 * (52/64), height=1.5, color=C_UTC, fill_opacity=0.3)
        high_bits_rect.align_to(full_long_bar, LEFT)
        
        low_bits_rect = Rectangle(width=12 * (12/64), height=1.5, color=C_TZ, fill_opacity=0.5)
        low_bits_rect.align_to(full_long_bar, RIGHT)

        brace_high = Brace(high_bits_rect, DOWN)
        txt_high = brace_high.get_text("High 52 bits: Millis UTC")
        
        brace_low = Brace(low_bits_rect, DOWN)
        txt_low = brace_low.get_text("Low 12 bits: TZ Key")

        self.play(
            Create(high_bits_rect), Write(brace_high), Write(txt_high),
            Create(low_bits_rect), Write(brace_low), Write(txt_low)
        )

        # Animation Sequence: Packing
        sample_millis = Text("Millis: 1698246000000", color=C_UTC, font_size=24).to_corner(UL).shift(DOWN*2)
        sample_tz = Text("TZ Key: 450", color=C_TZ, font_size=24).next_to(sample_millis, DOWN)
        self.play(Write(sample_millis), Write(sample_tz))

        # 1. Move Millis into position (Shift Left)
        millis_in_bar = Text("1698246000000", color=C_UTC, font_size=24).move_to(high_bits_rect.get_center())
        shift_op_txt = Text("<< 12 bits", color=C_UTC, font_size=30).next_to(full_long_bar, UP, buff=1)
        
        self.play(TransformFromCopy(sample_millis, millis_in_bar))
        self.play(Write(shift_op_txt))
        self.play(millis_in_bar.animate.shift(LEFT * 0.2)) # Subtle shift effect
        self.wait(0.5)

        # 2. Move Key into position (OR / Add)
        key_in_bar = Text("450", color=C_TZ, font_size=24).move_to(low_bits_rect.get_center())
        or_op_txt = Text("+ TimeZoneKey", color=C_TZ, font_size=30).next_to(shift_op_txt, RIGHT)

        self.play(TransformFromCopy(sample_tz, key_in_bar))
        self.play(Write(or_op_txt))
        self.wait(1)

        # Showing the resulting math
        final_math = Text("Packed = (MillisUTC << 12) + TimeZoneKey", font_size=32, color=YELLOW).to_edge(DOWN, buff=1)
        self.play(Write(final_math))
        self.wait(3)

        # Animation Sequence: Unpacking (Extraction)
        self.play(
            FadeOut(sample_millis), FadeOut(sample_tz), FadeOut(shift_op_txt), 
            FadeOut(or_op_txt), FadeOut(final_math)
        )
        
        
        unpacking_title = Text("Extracting Values (Unpacking)", font_size=24, color=RED).next_to(bar_label, UP)
        self.play(Write(unpacking_title))

        # Extract millis (Shift Right)
        extract_millis_arrow = Arrow(start=high_bits_rect.get_top(), end=high_bits_rect.get_top() + UP*1.5, color=C_UTC)
        extract_millis_op = Text(">> 12", color=C_UTC, font_size=24).next_to(extract_millis_arrow, RIGHT)
        extracted_millis_val = Text("= 1698246000000", color=C_UTC, font_size=24).next_to(extract_millis_op, RIGHT)

        self.play(GrowArrow(extract_millis_arrow), Write(extract_millis_op))
        self.play(TransformFromCopy(millis_in_bar, extracted_millis_val))

        # Extract key (Masking)
        extract_key_arrow = Arrow(start=low_bits_rect.get_bottom(), end=low_bits_rect.get_bottom() + DOWN*1.5, color=C_TZ)
        extract_key_op = Text("& 0xFFF (Mask)", color=C_TZ, font_size=24).next_to(extract_key_arrow, RIGHT)
        extracted_key_val = Text("= 450", color=C_TZ, font_size=24).next_to(extract_key_op, RIGHT)

        self.play(GrowArrow(extract_key_arrow), Write(extract_key_op))
        self.play(TransformFromCopy(key_in_bar, extracted_key_val))

        self.wait(3)

        # Cleanup Bit Packing Scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob not in [title, section_2_title]]
        )

        # Subsection 2B: Long Timestamp With TZ
        long_tz_txt = Text("Precision p > 3: LongTimestampWithTimeZone", font_size=28).next_to(section_2_title, DOWN)
        self.play(Write(long_tz_txt))

        long_tz_container = RoundedRectangle(width=10, height=3, corner_radius=0.2, color=C_OBJECT, fill_opacity=0.1).shift(DOWN * 0.5)
        long_tz_label = Text("Java Object Structure", font_size=20, color=C_OBJECT).next_to(long_tz_container, UP)

        f_millis = VGroup(Rectangle(width=3, height=1, color=C_UTC), Text("epochMillis\n(long)", font_size=18)).arrange(DOWN)
        f_picos = VGroup(Rectangle(width=3, height=1, color=C_PICO), Text("picosOfMilli\n(int)", font_size=18)).arrange(DOWN)
        f_key = VGroup(Rectangle(width=3, height=1, color=C_TZ), Text("timeZoneKey\n(short)", font_size=18)).arrange(DOWN)

        long_fields = VGroup(f_millis, f_picos, f_key).arrange(RIGHT, buff=0.3).move_to(long_tz_container)

        self.play(Create(long_tz_container), Write(long_tz_label))
        self.play(Create(long_fields), run_time=2)
        self.wait(3)
        
        self.play(FadeOut(Group(*self.mobjects)))