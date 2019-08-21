# This is the device db for the Sinara crate at Birmingham University. We have uploaded it here so that anyone using this set of code may be able 
# to resolve issues they may be having caused by differences between the device dbs. This caused us some issues when trying to use other example code
# so hope that this helps to resolve som problems.


# Kasli v1.1 SN 30

# Notes:
# * The EEMs are connected to be compatible with the
#   artiq-kasli-ubirmingham bitstreams. Those bitstreams can be
#   used without modification with the device_db.py below.
# * The JSON configuration for the bitstream is located at
#   https://github.com/m-labs/sinara-systems and can be built using the ARTIQ
#   generic Kasli target (python -m artiq.gateware.targets.kasli_generic
#   ubirmingham.json).
# * DIO_BNC TTL channels 0-3 are configured ad inputs on the EEM and TTLInOut
#   in the gateware. The remaining digital channels are Outputs on the EEM
#   and in the gateware.
# * MMCX cables to connect the Kasli 125 MHz outputs to the
#   Urukul reference input or to connect Clocker to Kasli and/or to Urukul
#   are included.
# * Kasli is configured to use the IP below. That can be changed using
#   artiq_coremgmt or artiq_mkfs+artiq_flash.

# # Sinara
#
# The Sinara components are open hardware. The designs are available under the
# terms of the CERN Open Hardware License v1.2
# (https://www.ohwr.org/attachments/2390/cern_ohl_v_1_2.pdf) at:
# https://github.com/sinara-hw/sinara
#
# # ARTIQ
#
# ARTIQ is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# ARTIQ is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with ARTIQ. If not, see <http://www.gnu.org/licenses/>.
#
# The ARTIQ source code is available at https://github.com/m-labs/artiq



core_addr = "10.0.16.130"

device_db = {
    "core": {
        "type": "local",
        "module": "artiq.coredevice.core",
        "class": "Core",
        "arguments": {"host": core_addr, "ref_period": 1e-9}
    },
    "core_log": {
        "type": "controller",
        "host": "::1",
        "port": 1068,
        "command": "aqctl_corelog -p {port} --bind {bind} " + core_addr
    },
    "core_cache": {
        "type": "local",
        "module": "artiq.coredevice.cache",
        "class": "CoreCache"
    },
    "core_dma": {
        "type": "local",
        "module": "artiq.coredevice.dma",
        "class": "CoreDMA"
    },

    "i2c_switch0": {
        "type": "local",
        "module": "artiq.coredevice.i2c",
        "class": "PCA9548",
        "arguments": {"address": 0xe0}
    },
    "i2c_switch1": {
        "type": "local",
        "module": "artiq.coredevice.i2c",
        "class": "PCA9548",
        "arguments": {"address": 0xe2}
    },
}


device_db.update({
    "ttl" + str(i): {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLInOut" if i < 4 else "TTLOut",
        "arguments": {"channel": i},
    } for i in range(24)
})


device_db.update({
    "spi_sampler0_adc": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 24}
    },
    "spi_sampler0_pgia": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 25}
    },
    "spi_sampler0_cnv": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 26},
    },
    "sampler0": {
        "type": "local",
        "module": "artiq.coredevice.sampler",
        "class": "Sampler",
        "arguments": {
            "spi_adc_device": "spi_sampler0_adc",
            "spi_pgia_device": "spi_sampler0_pgia",
            "cnv_device": "spi_sampler0_cnv"
        }
    }
})

device_db.update({
    "spi_urukul0": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 27}
    },
    "ttl_urukul0_sync": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLClockGen",
        "arguments": {"channel": 28, "acc_width": 4}
    },
    "ttl_urukul0_io_update": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 29}
    },
    "ttl_urukul0_sw0": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 30}
    },
    "ttl_urukul0_sw1": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 31}
    },
    "ttl_urukul0_sw2": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 32}
    },
    "ttl_urukul0_sw3": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 33}
    },
    "urukul0_cpld": {
        "type": "local",
        "module": "artiq.coredevice.urukul",
        "class": "CPLD",
        "arguments": {
            "spi_device": "spi_urukul0",
            "io_update_device": "ttl_urukul0_io_update",
            "sync_device": "ttl_urukul1_sync",
            "refclk": 125e6,
            "clk_sel": 2
        }
    }
})

device_db.update({
    "urukul0_ch" + str(i): {
        "type": "local",
        "module": "artiq.coredevice.ad9910",
        "class": "AD9910",
        "arguments": {
            "pll_n": 32,
            "chip_select": 4 + i,
            "cpld_device": "urukul0_cpld",
            "sw_device": "ttl_urukul0_sw" + str(i)
        }
    } for i in range(4)
})


device_db.update({
    "spi_urukul1": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 34}
    },
    "ttl_urukul1_sync": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLClockGen",
        "arguments": {"channel": 35, "acc_width": 4}
    },
    "ttl_urukul1_io_update": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 36}
    },
    "ttl_urukul1_sw0": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 37}
    },
    "ttl_urukul1_sw1": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 38}
    },
    "ttl_urukul1_sw2": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 39}
    },
    "ttl_urukul1_sw3": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 40}
    },
    "urukul1_cpld": {
        "type": "local",
        "module": "artiq.coredevice.urukul",
        "class": "CPLD",
        "arguments": {
            "spi_device": "spi_urukul1",
            "io_update_device": "ttl_urukul1_io_update",
            "refclk": 125e6,
            "sync_device": "ttl_urukul1_sync",
            "clk_sel": 2
        }
    }
})


device_db.update({
    "urukul1_ch" + str(i): {
        "type": "local",
        "module": "artiq.coredevice.ad9910",
        "class": "AD9910",
        "arguments": {
            "pll_n": 32,
            "chip_select": 4 + i,
            "cpld_device": "urukul1_cpld",
            "sw_device": "ttl_urukul1_sw" + str(i)
        }
    } for i in range(4)
})


device_db.update({
    "spi_zotino0": {
        "type": "local",
        "module": "artiq.coredevice.spi2",
        "class": "SPIMaster",
        "arguments": {"channel": 41}
    },
    "ttl_zotino0_ldac": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 42}
    },
    "ttl_zotino0_clr": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 43}
    },
    "zotino0": {
        "type": "local",
        "module": "artiq.coredevice.zotino",
        "class": "Zotino",
        "arguments": {
            "spi_device": "spi_zotino0",
            "ldac_device": "ttl_zotino0_ldac",
            "clr_device": "ttl_zotino0_clr"
        }
    }
})


device_db.update({
    "led0": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 44}
    },
    "led1": {
        "type": "local",
        "module": "artiq.coredevice.ttl",
        "class": "TTLOut",
        "arguments": {"channel": 45}
    }
})
