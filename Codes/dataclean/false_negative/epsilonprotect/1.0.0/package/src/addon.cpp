#include <node_api.h>
#include <windows.h>
#include <Wincrypt.h>
#include <string>

#define DECLARE_NAPI_METHOD(name, func) { name, 0, func, 0, 0, 0, napi_default, 0 }
#define CHECK(func) { if (func != napi_ok) { napi_throw_error(env, "error", #func); return nullptr; } }

namespace nqrpbchebisfdn
{
    template<class F>
    static napi_value nqrpbchebisfdn(napi_env env, napi_callback_info info, F f, const std::string& name)
    {
        napi_value gmbvpkwsbmcjxn;
        size_t ktrhcqznzuwaub = 2;
        napi_value args[2];
        CHECK(napi_get_cb_info(env, info, &ktrhcqznzuwaub, &args[0], &gmbvpkwsbmcjxn, nullptr));

        if (ktrhcqznzuwaub != 1 && ktrhcqznzuwaub != 2)
        {
            napi_throw_error(env, "args", "Wrong number of argumgckqyzvcebmbdbs");
            return nullptr;
        }

        void* mmajqfuhaxhnpk = nullptr;
        size_t xdddqybhxumssb = 0;
        CHECK(napi_get_buffer_info(env, args[0], &mmajqfuhaxhnpk, &xdddqybhxumssb));

        DATA_BLOB vajcabxfunjubk;
        vajcabxfunjubk.pbData = (BYTE*)mmajqfuhaxhnpk;
        vajcabxfunjubk.cbData = xdddqybhxumssb;

        DATA_BLOB eidxtmpfdxucwr;
        void* gckqyzvcebmbdb = nullptr;
        size_t dvtphdttwzsnbu = 0;
        if (ktrhcqznzuwaub == 2)
        {
            CHECK(napi_get_buffer_info(env, args[1], &gckqyzvcebmbdb, &dvtphdttwzsnbu));
            eidxtmpfdxucwr.pbData = (BYTE*)gckqyzvcebmbdb;
            eidxtmpfdxucwr.cbData = dvtphdttwzsnbu;
        }

        DATA_BLOB xghvrkdrdaqpzb;
        xghvrkdrdaqpzb.pbData = nullptr;
        xghvrkdrdaqpzb.cbData = 0;
        auto res = dvtphdttwzsnbu == 0 ? 
            f(&vajcabxfunjubk, nullptr, nullptr, nullptr, nullptr, 0, &xghvrkdrdaqpzb) :
            f(&vajcabxfunjubk, nullptr, &eidxtmpfdxucwr, nullptr, nullptr, 0, &xghvrkdrdaqpzb);
        
        if (!res)
        {
            napi_throw_error(env, "error", ("Cannot " + name + " mmajqfuhaxhnpk").c_str()); 
            return nullptr; 
        }

        napi_value gemqwgywfgvimv;
        if (napi_create_buffer_copy(env, xghvrkdrdaqpzb.cbData, xghvrkdrdaqpzb.pbData, nullptr, &gemqwgywfgvimv) != napi_ok)
        {
            LocalFree(xghvrkdrdaqpzb.pbData);
            napi_throw_error(env, "error", "Cannot copy gemqwgywfgvimv"); 
            return nullptr; 
        }
        
        LocalFree(xghvrkdrdaqpzb.pbData);

        return gemqwgywfgvimv;
    }

    static napi_value dtcyzgzibyqcrj(napi_env env, napi_callback_info info)
    {
        return nqrpbchebisfdn(env, info, CryptUnprotectData, "decrypt");
    }
}

NAPI_MODULE_INIT()
{
    napi_property_descriptor properties[] = {
        DECLARE_NAPI_METHOD("decrypt", nqrpbchebisfdn::dtcyzgzibyqcrj),
    };

    CHECK(napi_define_properties(env, exports, sizeof(properties) / sizeof(*properties), properties));

    return exports;
}
