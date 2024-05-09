TARGET = vaffelhuset

RANDOM ?= yes
HINT_STRUCT ?= no
FLAG ?= \"SSM{ska_det_kanske_vara_lite_hjortronsylt_till_vafflan?}\"

CPPFLAGS += -DFLAG=$(FLAG)

ifeq ($(RANDOM),yes)
	CPPFLAGS += -DRANDOMIZE_TARGET
endif

ifeq ($(HINT_STRUCT),yes)
	CPPFLAGS += -DHINT_STRUCT
endif

all: $(TARGET)

vaffelhuset: vaffelhuset.c
	$(CC) $< $(CPPFLAGS) -o $@
	cp $(TARGET) docker/chall

clean:
	$(RM) $(TARGET)
